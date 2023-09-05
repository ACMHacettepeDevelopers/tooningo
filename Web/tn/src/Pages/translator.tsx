import { useState } from "react";
import { storage } from "../Config/firebase";
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { v4 } from "uuid";
import axios from "axios";

export const Translator = () => {
  const [imageUpload, setImageUpload] = useState(null);
  const [imageUrl, setImageUrl] = useState("");

  const uploadFile = () => {
    if (imageUpload == null) return;
    const imageRef = ref(storage, `images/${imageUpload.name + v4()}`); //Random file name generator. Error at .name is OK
    uploadBytes(imageRef, imageUpload).then((snapshot) => {
      getDownloadURL(snapshot.ref).then((url) => {
        setImageUrl(url);
      });
    });
    alert("Image Uploaded");
  };

  const sendData = (url: string) => {
    axios
      .post("http://your-python-backend-url/api/endpoint", {
        userInput: url,
      })
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  //User upload image with uploadFile method. Image is stored in Firebase Storage, which every image has public URL
  //imageUrl is the URL to the image. Use this URL to start backend operations.

  return (
    <>
      <div className="paragraph">
        Translator: Çevirinin yapılıp sonucun verildiği, kodun bağlandığı sayfa
        / Hesap başına 100 kullanım gibi özellikler eklenebilir
      </div>
      <div>
        <input
          className="button"
          type="file"
          onChange={(event) => {
            setImageUpload(event.target.files[0]); //Error is ok
          }}
        />
        <button className="button" onClick={uploadFile}>
          Upload Image
        </button>
        <button className="button" onClick={() => console.log(imageUrl)}>
          See Url In Console
        </button>
        <img src={imageUrl} alt="" />
      </div>
    </>
  );
};
