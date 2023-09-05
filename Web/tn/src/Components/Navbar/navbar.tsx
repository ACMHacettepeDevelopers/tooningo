import { Link} from "react-router-dom";
import { auth } from "../../Config/firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import { signOut } from "firebase/auth";
import { useNavigate } from "react-router-dom";


export const Navbar = () => {
  const [user, loading, errors] = useAuthState(auth);
  const navigate = useNavigate();


  const signUserOut = async () => {
    await signOut(auth);
    navigate("/about_acm")
  };
  return (
    <div className="navbar">
      <Link to={"/"} className="logo">
        Tooningo
      </Link>

      <nav className="links">
        <img src="./toon.jpg" alt="" />
        <Link to={"/"}> Home </Link>
        {user ? (
          <Link to={"/translator"}> Translator </Link>
        ) : (
          <Link to={"/login"}> Login </Link>
        )}
        <Link to={"/contact"}> Contact </Link>
        <Link to={"/about_acm"}> About ACM </Link>
      </nav>
      <div className="user">
        {user && (
          <>
            <img src={user?.photoURL || ""} width="20" height="20" />
            <p> {user?.displayName} </p>
            <button onClick={signUserOut} > 
            Log Out
            </button>
            
          </>
        )}
      </div>
    </div>
  );
};
