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
} from "firebase/auth"

const firebaseConfig = {
  apiKey: "AIzaSyBbeyWpC0nEEuZIuK5eONt0LDGYuKm038Q",
  authDomain: "zawani-aeba8.firebaseapp.com",
  projectId: "zawani-aeba8",
  storageBucket: "zawani-aeba8.firebasestorage.app",
  messagingSenderId: "720010119224",
  appId: "1:720010119224:web:5ec800f4f49883bbb43ecd",
}

const app = initializeApp(firebaseConfig)
const auth = getAuth(app)
const googleProvider = new GoogleAuthProvider()

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
}
export default app
