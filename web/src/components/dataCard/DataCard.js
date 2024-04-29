import React from 'react';
import './DataCard.css';

const DataCard = ({ data }) => {
  return (
    <div className="card">
      <div className="content">
        <p><strong>Learning Rate:</strong> {data.learning_rate}</p>
        <p><strong>Number of Convolutional Layers:</strong> {data.num_conv_layers}</p>
        <p><strong>Kernel Sizes:</strong> {data.kernel_sizes.join(', ')}</p>
        <p><strong>Filters:</strong> {data.filters.join(', ')}</p>
        <p><strong>Fully connected Layers:</strong> {data.fully_connected}</p>
        <p><strong>Dropout:</strong> {data.dropout}</p>
        <p><strong>Accuracy:</strong> {data.fitness.toFixed(4)}</p>
      </div>
    </div>
  );
}

export default DataCard;
