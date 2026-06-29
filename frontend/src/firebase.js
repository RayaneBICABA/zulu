import { initializeApp } from "firebase/app"
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  GoogleAuthProvider,
  signInWithRedirect,
  getRedirectResult,
  signInWithCredential,
  sendPasswordResetEmail,
} from "firebase/auth"

const firebaseConfig = {
  apiKey: "AIzaSyBbeyWpC0nEEuZIuK5eONt0LDGYuKm038Q",
  authDomain: "zawani-aeba8.firebaseapp.com",
  projectId: "zawani-aeba8",
  storageBucket: "zawani-aeba8.firebasestorage.app",
  messagingSenderId: "720010119224",
  appId: "1:720010119224:web:5ec800f4f49883bbb43ecd",
}

let app, auth, googleProvider
try {
  app = initializeApp(firebaseConfig)
  auth = getAuth(app)
  googleProvider = new GoogleAuthProvider()
} catch (e) {
  console.error('Firebase init failed:', e)
}

export {
  auth,
  googleProvider,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  signInWithRedirect,
  getRedirectResult,
  signInWithCredential,
  sendPasswordResetEmail,
}
export default app
