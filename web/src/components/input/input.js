import React, { useState } from 'react';
import './input.css';
import { RESULT, UPLOAD } from './enpoints';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import DataCard from '../dataCard/DataCard';
import CircuitAnimation from '../Animation/CircuitAnimation';

function InputBox() {
    const [username, setUsername] = useState('');
    const [file, setFile] = useState(null); // Cambiado para manejar archivo
    const [email, setEmail] = useState('');
    const [numDesc, setNumDesc] = useState('');
    const [numEpochs, setNumEpochs] = useState('');
    const [numClases, setNumClases] = useState('')
    const [splitted, setSplitted] = useState('')
    const [sol, setSol] = useState(false)
    const [result, setResult] = useState("Still working on it")
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
        if (splitted === "yes") {
            setSplitted("no");
        } else {
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
        formData.append('file', file);
        formData.append('num_clases', numClases);
        formData.append('splitted', splitted);

        fetch(UPLOAD, {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                toast.info("We have queued your request, come back later, the process will take");
                return response.json();
            })
            .then(data => console.log(data))
            .catch(error => {
                console.error('Error:', error);
                toast.error("An error has been found during your request, try again later");
            });
    };

    const handleSubmitStatus = (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('username', username);
        formData.append('email', email);
        fetch(RESULT, {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if ("dropout" in data.message) {
                    setResult(data.message)
                    toast.success("The algorythm has been finished")
                    setSol(true)
                } else {
                    if("error" in data.message){
                        toast.error(data.message.error)
                        setResult(data.message.error)
                        setSol(false)
                    }else{
                    toast.info(data.message.Aux)
                    setResult(data.message.Aux)
                    setSol(false)
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);

                toast.error("An error has been found during your request, try again later");
            });
    };

    return (
        <div className='container'>
            <CircuitAnimation />
            <div className="login-box">
                <h2> Search the best architecture</h2>
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
            <div className="login-box">
                <h2> Check the results </h2>
                <form onSubmit={handleSubmitStatus}>
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
                    <button type="submit" className="cta">
                        <span className="hover-underline-animation"> check results </span>
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
                    {sol && <DataCard data={result} />}
                </form>
            </div>
            <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={true}
                rtl={false}
                pauseOnFocusLoss
                pauseOnHover
            />
        </div>
    );
}

export default InputBox;
