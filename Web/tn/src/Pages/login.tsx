import { auth, provider } from "../Config/firebase";
import { signInWithPopup } from "firebase/auth";
import { useNavigate } from "react-router-dom";

export const Login = () => {
    const navigate = useNavigate();

    const signInWithGoogle = async () => {
        const result = await signInWithPopup(auth, provider);
        console.log(result);
        navigate("/translator");
      };

    return(
        <div>
            <h1>Login: Devam etmek için login yapmak gerekiyor</h1>

            <button onClick={signInWithGoogle} className="button">Continue With Google</button>

            
        </div>
    )
}