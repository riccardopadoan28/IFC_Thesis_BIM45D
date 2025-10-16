import * as THREE from './vendor/three.module.js';
import { OrbitControls } from './vendor/OrbitControls.js';
import { IFCLoader } from './vendor/IFCLoader.js';

// Collega il componente Streamlit
const { Streamlit } = window;

// Variabili globali
let scene, camera, renderer, controls, ifcLoader;

function initViewer(url) {
  // Scene
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xaaaaaa);

  // Camera
  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(8, 13, 15);

  // Renderer
  renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("three-canvas") });
  renderer.setSize(window.innerWidth, window.innerHeight);

  // Controls
  controls = new OrbitControls(camera, renderer.domElement);

  // Light
  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(10, 10, 10);
  scene.add(light);

  // IFC Loader
  ifcLoader = new IFCLoader();
  ifcLoader.ifcManager.setWasmPath("./vendor/IFC/");

  ifcLoader.load(url, (ifcModel) => {
    scene.add(ifcModel);
    animate();
  });
}

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

// 👉 Riceve i dati da Streamlit
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, (event) => {
  const { url } = event.detail.args;
  if (url) {
    initViewer(url);
  }
  Streamlit.setFrameHeight(window.innerHeight);
});

// Primo render
Streamlit.setComponentReady();
Streamlit.setFrameHeight(window.innerHeight);