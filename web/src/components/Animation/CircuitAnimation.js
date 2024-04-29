import React from 'react';
import './CircuitAnimation.css';

const CircuitAnimation = () => {
    const numberOfLines = 30; // Define cuántas líneas quieres
    const lines = [];
  
    for (let i = 0; i < numberOfLines; i++) {
      const top = Math.random() * 100;
      const left = Math.random() * 100;
      const rotation = Math.random() * 360;
      lines.push(
        <div key={i} className="circuit-line" style={{
          top: `${top}%`,
          left: `${left}%`,
          transform: `rotate(${rotation}deg)`
        }}></div>
      );
    }
  
    return (
      <div className="circuit-board">
        {lines}
      </div>
    );
}

export default CircuitAnimation;
