import React, { useState } from 'react';
import './input.css';
import { RESULT, UPLOAD } from './enpoints';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import DataCard from '../dataCard/DataCard';
import TextGenerateEffect from '../describe/generateText';
import { Input } from 'postcss';
import Label from './label';
import Input2 from './input2';

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
                    if ("error" in data.message) {
                        toast.error(data.message.error)
                        setResult(data.message.error)
                        setSol(false)
                    } else {
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
            <div className="max-w-md w-full mx-auto rounded-2xl p-4 md:p-8 shadow-input bg-white dark:bg-black">
                <h2 className="font-bold text-xl text-neutral-800 dark:text-neutral-200 mb-2 text-center">
                    Search the best architecture
                </h2>
                <p className="text-neutral-600 text-sm max-w-sm dark:text-neutral-300 mb-4 text-center">
                    <TextGenerateEffect
                        words={"Introduce your data"}
                        className="font-extralight text-base md:text-4xl dark:text-neutral-200 py-2"
                    />
                </p>
                <form className="my-4" onSubmit={handleSubmit}>
                    <div className="mb-2">
                        <Label htmlFor="name">Name</Label>
                        <Input2
                            type="text"
                            name="username"
                            required
                            value={username}
                            onChange={handleUsernameChange}
                        />
                    </div>
                    <div className="mb-2">
                        <Label htmlFor="name">Email</Label>
                        <Input2
                            type="email"
                            name="email"
                            required
                            value={email}
                            onChange={handleEmailChange}
                        />
                    </div>
                    <div className="mb-2">
                        <Label htmlFor="name">Number of descendency</Label>
                        <Input2
                            type="text"
                            name="numDesc"
                            required
                            value={numDesc}
                            onChange={handleNumDescChange}
                        />
                    </div>
                    <div className="mb-2">
                        <Label htmlFor="name">Number of epochs</Label>
                        <Input2
                            type="text"
                            name="numEpochs"
                            required
                            value={numEpochs}
                            onChange={handleNumEpochsChange}
                        />
                    </div>
                    <div className="mb-2">
                        <Label htmlFor="name">Number of classes</Label>
                        <Input2
                            type="text"
                            name="numEpochs"
                            required
                            value={numClases}
                            onChange={handleNumClases}
                        />
                    </div>
                    <div className="mb-2">
                        <input
                            className='cyberpunk-checkbox'
                            type="checkbox"
                            name="splitted"
                            required
                            value={splitted}
                            onChange={handleSplitted}
                        />
                        <Label>Is it splitted into train and test?</Label>
                    </div>
                    <div className="mb-2">
                        <input
                            type="file"
                            name="data"
                            required
                            onChange={handleFileChange}
                        />
                    </div>
                    <div className="flex justify-center">
                            <button
                                className="relative inline-flex h-12 overflow-hidden rounded-full p-[1px] focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50 dark:focus:ring-offset-slate-800 transition-all duration-300 hover:bg-slate-950 dark:hover:bg-slate-100"
                                type="submit"
                            >
                                <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
                                <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-full bg-slate-100 dark:bg-slate-950 px-6 py-2 text-sm font-medium text-black dark:text-white backdrop-blur-3xl transition-all duration-300 hover:bg-slate-950 hover:text-white dark:hover:bg-slate-100 dark:hover:text-black">
                                    Work your magic &rarr;
                                </span>
                            </button>
                        </div>
                </form>
            </div>
            <div className="max-w-md w-full mx-auto rounded-2xl p-4 md:p-8 shadow-input bg-white dark:bg-black">
            <h2 className="font-bold text-xl text-neutral-800 dark:text-neutral-200 mb-2 text-center">
                 Check the results, please notice it could take several hours </h2>
                 <form className="my-4" onSubmit={handleSubmitStatus}>
                    <div className="mb-2">
                        <Label htmlFor="name">Name</Label>
                        <Input2
                            type="text"
                            name="username"
                            required
                            value={username}
                            onChange={handleUsernameChange}
                        />
                    </div>
                    <div className="mb-2">
                        <Label htmlFor="name">Email</Label>
                        <Input2
                            type="email"
                            name="email"
                            required
                            value={email}
                            onChange={handleEmailChange}
                        />
                    </div>
                    <div className="flex justify-center">
                            <button
                                className="relative inline-flex h-12 overflow-hidden rounded-full p-[1px] focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50 dark:focus:ring-offset-slate-800 transition-all duration-300 hover:bg-slate-950 dark:hover:bg-slate-100"
                                type="submit"
                            >
                                <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
                                <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-full bg-slate-100 dark:bg-slate-950 px-6 py-2 text-sm font-medium text-black dark:text-white backdrop-blur-3xl transition-all duration-300 hover:bg-slate-950 hover:text-white dark:hover:bg-slate-100 dark:hover:text-black">
                                    check results &rarr;
                                </span>
                            </button>
                        </div>
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
