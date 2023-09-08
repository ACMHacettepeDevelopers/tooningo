import { useState } from 'react';

export const Translatorv2 = () => {
  const [inputValue, setInputValue] = useState('');
  const [result, setResult] = useState(null);

  const handleInputChange = (e: any) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000//getter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ urlink: inputValue }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data.result);
      } else {
        throw new Error('Aga olmadi');
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="App">
      <h1 className='headings'>Enter Webtoon Url</h1>
      <input
        type="text"
        placeholder="Enter a webtoon URL"
        value={inputValue}
        onChange={handleInputChange}
        className='button'
      />
      <button className='button' onClick={handleSubmit}>Upload</button>
      {result !== null && <p className='paragraph'>{result}</p>}
    </div>
  );
}

