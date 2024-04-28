import React, { useState } from 'react';
import './input.css';
import { UPLOAD } from './enpoints';

function InputBox() {
    const [username, setUsername] = useState('');
    const [file, setFile] = useState(null); // Cambiado para manejar archivo
    const [email, setEmail] = useState('');
    const [numDesc, setNumDesc] = useState('');
    const [numEpochs, setNumEpochs] = useState('');
    const [numClases, setNumClases] = useState('')
    const [splitted, setSplitted] = useState('')

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handleFileChange = (event) => {
        setFile(event.target.files[0]); // Manejo de archivo
    };

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handleNumDescChange = (event) => {
        setNumDesc(event.target.value);
    };

    const handleNumEpochsChange = (event) => {
        setNumEpochs(event.target.value);
    };

    const handleNumClases = (event) => {
        setNumClases(event.target.value);
    };

    const handleSplitted = (event) => {
        if(splitted === "yes"){
            setSplitted("no");
        }else{
            setSplitted("yes");
        }
    };


    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('username', username);
        formData.append('email', email);
        formData.append('numDesc', numDesc);
        formData.append('numEpochs', numEpochs);
        formData.append('file', file); // Agregar el archivo al FormData
        formData.append('num_clases', numClases)
        formData.append('splitted', splitted)
        fetch(UPLOAD, { // Ajusta la URL según sea necesario
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    };

    return (
        <div className="login-box">
            <form onSubmit={handleSubmit}>
                <div className="user-box">
                    <input
                        type="text"
                        name="username"
                        required
                        value={username}
                        onChange={handleUsernameChange}
                    />
                    <label>Username</label>
                </div>
                <div className="user-box">
                    <input
                        type="email"
                        name="email"
                        required
                        value={email}
                        onChange={handleEmailChange}
                    />
                    <label>Email</label>
                </div>
                <div className="user-box">
                    <input
                        type="text"
                        name="numDesc"
                        required
                        value={numDesc}
                        onChange={handleNumDescChange}
                    />
                    <label>Number of descendency</label>
                </div>
                <div className="user-box">
                    <input
                        type="text"
                        name="numEpochs"
                        required
                        value={numEpochs}
                        onChange={handleNumEpochsChange}
                    />
                    <label>Number of epochs</label>
                </div>
                <div className="user-box">
                    <input
                        type="text"
                        name="numEpochs"
                        required
                        value={numClases}
                        onChange={handleNumClases}
                    />
                    <label>Number of classes</label>
                </div>
                <div className="cyberpunk-checkbox-label">
                    <input
                        className='cyberpunk-checkbox'
                        type="checkbox"
                        name="splitted"
                        required
                        value={splitted}
                        onChange={handleSplitted}
                    />
                    <label>Is it splitted into train and test?</label>
                </div>
                <div className="user-box">
                    <input
                        type="file"
                        name="data"
                        required
                        onChange={handleFileChange}
                    />
                </div>
                <button type="submit" className="cta">
                    <span className="hover-underline-animation"> work your magic </span>
                    <svg
                        id="arrow-horizontal"
                        xmlns="http://www.w3.org/2000/svg"
                        width="30"
                        height="10"
                        viewBox="0 0 46 16"
                    >
                        <path
                            id="Path_10"
                            data-name="Path 10"
                            d="M8,0,6.545,1.455l5.506,5.506H-30V9.039H12.052L6.545,14.545,8,16l8-8Z"
                            transform="translate(30)"
                        ></path>
                    </svg>
                </button>
            </form>
        </div>
    );
}

export default InputBox;
