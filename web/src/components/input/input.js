import React, { useState } from 'react';
import './input.css'; // Asegúrate de que este archivo CSS está en el mismo directorio que tu componente

function InputBox() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault(); // Previene el envío del formulario
        console.log('Username:', username, 'Password:', password);
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
                        type="password"
                        name="password"
                        required
                        value={password}
                        onChange={handlePasswordChange}
                    />
                    <label>Dataset to search</label>
                </div>
                <center>
                    <a>
                        <span>_</span>
                        <b type="submit" className="login-button">SEND</b>
                    </a>
                </center>
            </form>
        </div>
    );
}

export default InputBox;
