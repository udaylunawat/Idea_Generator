import React, { useState } from "react";
import Card from "./component/Card";
import './App.css'
import Input from "./component/Input";
import axios from 'axios';
import { testJson } from "./utils";

function App() {
  const [jsonData, setJsonData] = useState({});
  const [inputText, setInputText] = useState("");

  const fetchData = async () => {
    const { data } = await axios.post('http://localhost:5000/get_result', { inputText });
    console.log(data);
    setJsonData(data);
  };

  const handleInputTextChange = (e) => {
    setInputText(e.target.value);
  }

  const handleButtonClick = () => {
    fetchData();
  }

  const handleDemoClick = () => {
    console.log(testJson);
    setJsonData(testJson);
  }

  return (
    <>
      <div className="maincontainer">
        <div>
          <Input onInputChange={handleInputTextChange} onButtonClick={handleButtonClick} onDemoClick={handleDemoClick} />
        </div>
        <div>
          <Card data={jsonData} />
        </div>
      </div>
    </>
  );
}

export default App;






// import React, { useState } from "react";
// import Card from "./component/Card";
// import './App.css'
// import Input from "./component/Input";
// import axios from 'axios';

// function App() {
//   const [jsonData, setJsonData] = useState({});
//   const [inputText, setInputText] = useState("");

//   const fetchData = async () => {
//     const { data } = await axios.post('http://localhost:5000/get_result', { inputText });
//     console.log(data);
//     setJsonData(data);
//   };

//   const handleInputTextChange = (e) => {
//     setInputText(e.target.value);
//   }

//   const handleButtonClick = () => {
//     fetchData();
//   }

//   return (
//     <>
//       <div className="maincontainer">
//         <div>
//           <Input onInputChange={handleInputTextChange} onButtonClick={handleButtonClick} />
//         </div>
//         <div>
//           <Card data={jsonData} />
//         </div>
//       </div>
//     </>
//   );
// }

// export default App;
