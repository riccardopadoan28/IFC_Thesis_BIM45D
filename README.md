## Temporary files
- All temporary artifacts are now stored in the `temp/` folder at the project root.
- Legacy folders that were previously used (downloads, temp_downloads, temp-download) are deprecated and can be removed.
- To consolidate and clean up legacy temporary folders run:

  python -m tools.pathhelper

- To also delete `static/temp_model.ifc` after consolidation:

  python -m tools.pathhelper --remove-static-temp


### USE THIS LINE TO INSTALL ALL THE DEPENDENCIES 
pip install -r requirements.txt


## USE THIS LINE TO RUN THE APPLICATION
python -m streamlit run Home.py