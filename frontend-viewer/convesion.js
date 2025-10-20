#!/usr/bin/env node
// Wrapper to convert IFC -> XKT using xeokit convert2xkt
// Usage flags: -s/--source, -o/--output, -p/--properties, -m/--metamodel, -l/--log, -h/--help

const fs = require('fs');
const path = require('path');
const convert2xkt = require('@xeokit/xeokit-xkt-utils/dist/convert2xkt.cjs.js');

function usage() {
  const msg = `Usage: node convesion.js [options]\n\n` +
`Options:\n\n` +
`  -s, --source [file]      path to source IFC/GLTF/etc. file (required)\n` +
`  -o, --output [file]      path to target .xkt file (required)\n` +
`  -p, --properties [dir]   target directory for object property files (optional)\n` +
`  -m, --metamodel [file]   path to source metamodel JSON file (optional)\n` +
`  -l, --log                enable logging\n` +
`  -h, --help               show this help\n`;
  console.log(msg);
}

function parseArgs(argv) {
  const args = { log: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    switch (a) {
      case '-h':
      case '--help':
        args.help = true; break;
      case '-l':
      case '--log':
        args.log = true; break;
      case '-s':
      case '--source':
        args.source = argv[++i]; break;
      case '-o':
      case '--output':
        args.output = argv[++i]; break;
      case '-p':
      case '--properties':
        args.properties = argv[++i]; break;
      case '-m':
      case '--metamodel':
        args.metamodel = argv[++i]; break;
      default:
        break;
    }
  }
  return args;
}

(async () => {
  const args = parseArgs(process.argv);
  if (args.help) { usage(); process.exit(0); }
  if (!args.source || !args.output) {
    console.error('Error: --source and --output are required.');
    usage();
    process.exit(1);
  }

  const sourcePath = path.resolve(args.source);
  const outputPath = path.resolve(args.output);
  const outputDir = path.dirname(outputPath);

  if (!fs.existsSync(sourcePath)) {
    console.error(`Source not found: ${sourcePath}`);
    process.exit(1);
  }
  fs.mkdirSync(outputDir, { recursive: true });

  const opts = {
    source: sourcePath,
    target: outputPath,
    log: !!args.log
  };

  if (args.properties) {
    const propsDir = path.resolve(args.properties);
    fs.mkdirSync(propsDir, { recursive: true });
    opts.properties = propsDir;
  }

  if (args.metamodel) {
    const mmPath = path.resolve(args.metamodel);
    if (fs.existsSync(mmPath)) {
      try { opts.metaModel = JSON.parse(fs.readFileSync(mmPath, 'utf-8')); }
      catch (e) { console.warn(`Warning: failed to parse metamodel JSON: ${e.message}`); }
    } else {
      console.warn(`Warning: metamodel file not found at ${mmPath}`);
    }
  }

  const t0 = Date.now();
  if (opts.log) {
    try {
      const stats = fs.statSync(sourcePath);
      console.log(`[convesion] Reading input file: ${path.basename(sourcePath)}`);
      console.log(`[convesion] Input file size: ${(stats.size/1024).toFixed(2)} kB`);
      console.log(`[convesion] Converting...`);
    } catch(_) {}
  }

  try {
    await convert2xkt(opts);
    const dt = (Date.now() - t0) / 1000;
    if (opts.log) {
      try {
        const size = fs.statSync(outputPath).size;
        console.log(`[convesion] Writing XKT file: ${outputPath}`);
        console.log(`[convesion] XKT size: ${(size/1024).toFixed(2)} kB`);
      } catch(_) {}
      console.log(`[convesion] Conversion time: ${dt.toFixed(2)} s`);
    }
    process.exit(0);
  } catch (e) {
    console.error('Conversion failed:');
    console.error(e && e.stack ? e.stack : e);
    process.exit(1);
  }
})();
