"""
Helper for IFC Validation using buildingSMART official validation checks.

Uso: Integrates official validation checks from buildingSMART/validate repository
Funzioni:
- validate_ifc_syntax(ifc_path): Syntax validation
- validate_ifc_schema(ifc_path): Schema validation  
- validate_ifc_rules(ifc_path, rule_types): Gherkin rules validation
- run_all_validations(ifc_path): Runs all checks
"""

from __future__ import annotations
from typing import Any, Dict, List, Tuple, Optional
import subprocess
import json
import tempfile
import os
import ifcopenshell


def validate_ifc_syntax(ifc_path: str) -> Dict[str, Any]:
    """
    Run Syntax Validation using ifcopenshell.
    
    Returns dict with: ok, errors, warnings
    """
    try:
        # Try to open the file - basic syntax check
        model = ifcopenshell.open(ifc_path)
        return {
            "ok": True,
            "errors": [],
            "warnings": [],
            "message": "Syntax validation passed"
        }
    except Exception as e:
        return {
            "ok": False,
            "errors": [str(e)],
            "warnings": [],
            "message": f"Syntax validation failed: {e}"
        }


def validate_ifc_schema(ifc_path: str) -> Dict[str, Any]:
    """
    Run Schema Validation using ifcopenshell.validate.
    
    Returns dict with: ok, errors, warnings
    """
    try:
        # Use ifcopenshell.validate module if available
        result = subprocess.run(
            ["python", "-m", "ifcopenshell.validate", "--json", "--rules", "--fields", ifc_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                errors = data.get("errors", [])
                warnings = data.get("warnings", [])
                return {
                    "ok": len(errors) == 0,
                    "errors": errors,
                    "warnings": warnings,
                    "message": "Schema validation completed"
                }
            except json.JSONDecodeError:
                # If output is not JSON, treat as success if return code is 0
                return {
                    "ok": True,
                    "errors": [],
                    "warnings": [result.stdout] if result.stdout else [],
                    "message": "Schema validation completed (non-JSON output)"
                }
        else:
            # Return code non-zero means errors
            try:
                data = json.loads(result.stdout)
                errors = data.get("errors", [])
                warnings = data.get("warnings", [])
                return {
                    "ok": False,
                    "errors": errors,
                    "warnings": warnings,
                    "message": "Schema validation found errors"
                }
            except json.JSONDecodeError:
                return {
                    "ok": False,
                    "errors": [result.stdout or "Unknown schema error"],
                    "warnings": [],
                    "message": "Schema validation failed"
                }
    except FileNotFoundError:
        return {
            "ok": False,
            "errors": ["ifcopenshell.validate module not available"],
            "warnings": [],
            "message": "Schema validation not available"
        }
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "errors": ["Schema validation timed out"],
            "warnings": [],
            "message": "Schema validation timed out"
        }
    except Exception as e:
        return {
            "ok": False,
            "errors": [str(e)],
            "warnings": [],
            "message": f"Schema validation error: {e}"
        }


def validate_ifc_gherkin_rules(ifc_path: str, rule_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Run Gherkin Rules Validation.
    
    Args:
        ifc_path: Path to IFC file
        rule_types: List of rule types to check (CRITICAL, IMPLEMENTER_AGREEMENT, INFORMAL_PROPOSITION, INDUSTRY_PRACTICE)
    
    Returns dict with: ok, errors, warnings, rule_results
    """
    if rule_types is None:
        rule_types = ["CRITICAL"]
    
    all_results = []
    all_errors = []
    all_warnings = []
    
    for rule_type in rule_types:
        try:
            # Try to run gherkin rules if available
            # NOTE: This assumes buildingSMART/ifc-gherkin-rules is available
            result = subprocess.run(
                ["python", "-m", "ifc_validation.checks.check_gherkin", 
                 "--file-name", ifc_path, 
                 "--rule-type", rule_type],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                rule_result = {
                    "rule_type": rule_type,
                    "status": "passed",
                    "details": result.stdout or "No issues found"
                }
                all_results.append(rule_result)
            else:
                rule_result = {
                    "rule_type": rule_type,
                    "status": "failed",
                    "details": result.stdout or result.stderr or "Validation failed"
                }
                all_results.append(rule_result)
                all_errors.append(f"{rule_type}: {result.stdout or result.stderr}")
                
        except FileNotFoundError:
            all_warnings.append(f"Gherkin rules checker not available for {rule_type}")
        except subprocess.TimeoutExpired:
            all_errors.append(f"Gherkin rules validation timed out for {rule_type}")
        except Exception as e:
            all_errors.append(f"Gherkin rules validation error for {rule_type}: {e}")
    
    return {
        "ok": len(all_errors) == 0,
        "errors": all_errors,
        "warnings": all_warnings,
        "rule_results": all_results,
        "message": f"Gherkin rules validation completed for {len(rule_types)} rule types"
    }


def run_all_validations(ifc_path: str, rule_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Run all available validation checks.
    
    Args:
        ifc_path: Path to IFC file
        rule_types: List of Gherkin rule types to check
    
    Returns dict with: overall_ok, syntax, schema, gherkin, summary
    """
    results = {
        "syntax": validate_ifc_syntax(ifc_path),
        "schema": validate_ifc_schema(ifc_path),
        "gherkin": validate_ifc_gherkin_rules(ifc_path, rule_types)
    }
    
    overall_ok = all([
        results["syntax"]["ok"],
        results["schema"]["ok"],
        results["gherkin"]["ok"]
    ])
    
    total_errors = sum([
        len(results["syntax"]["errors"]),
        len(results["schema"]["errors"]),
        len(results["gherkin"]["errors"])
    ])
    
    total_warnings = sum([
        len(results["syntax"]["warnings"]),
        len(results["schema"]["warnings"]),
        len(results["gherkin"]["warnings"])
    ])
    
    results["overall"] = {
        "ok": overall_ok,
        "total_errors": total_errors,
        "total_warnings": total_warnings,
        "message": f"Validation complete: {total_errors} errors, {total_warnings} warnings"
    }
    
    return results


def validate_ifc_from_model(ifc_model: Any) -> Dict[str, Any]:
    """
    Validate an IFC file from an ifcopenshell model object.
    
    Creates a temporary file and runs validations.
    """
    temp_path = None
    try:
        # Write model to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ifc") as f:
            temp_path = f.name
        
        ifc_model.write(temp_path)
        
        # Run validations on temp file
        results = run_all_validations(temp_path)
        
        return results
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception:
                pass

