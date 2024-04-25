import React, { useState } from 'react';
import './input.css'; // Asegúrate de que este archivo CSS está en el mismo directorio que tu componente

function InputBox() {
    const [username, setUsername] = useState('');
    const [data, setData] = useState('');
    const [email, setEmail] = useState('');

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handleData = (event) => {
        setData(event.target.value);
    };

    const handleEmail = (event) => {
        setEmail(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault(); // Previene el envío del formulario
        console.log('Username:', username, 'Data:', data, 'Email: ', email);
        // Aquí puedes añadir la lógica para verificar las credenciales, etc.
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
                        onChange={handleEmail}
                    />
                    <label>Email</label>
                </div>
                <div className="user-box">
                    <input
                        type="text"
                        name="data"
                        required
                        value={data}
                        onChange={handleData}
                    />
                    <label>Data</label>
                </div>
                <button class="cta">
                    <span class="hover-underline-animation"> work your magic </span>
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
