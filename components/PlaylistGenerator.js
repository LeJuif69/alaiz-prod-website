import React, { useState } from 'react';

const PlaylistGenerator = () => {
  const [playlist, setPlaylist] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generatePlaylist = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/playlist/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error('Erreur lors de la génération de la playlist');
      }
      
      const data = await response.json();
      setPlaylist(data.playlist);
      setMetadata(data.metadata);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="playlist-generator">
      <h2>Générateur de Playlist</h2>
      
      <button 
        onClick={generatePlaylist} 
        disabled={loading}
        className="btn-generate"
      >
        {loading ? 'Génération en cours...' : 'Générer une playlist'}
      </button>
      
      {error && (
        <div className="error-message">
          <p>Erreur: {error}</p>
        </div>
      )}
      
      {metadata && (
        <div className="playlist-metadata">
          <h3>Métadonnées</h3>
          <div className="metadata-info">
            <p><strong>Titre:</strong> {metadata.title}</p>
            <p><strong>Description:</strong> {metadata.description}</p>
            <p><strong>Nombre de pistes:</strong> {metadata.trackCount}</p>
          </div>
        </div>
      )}
      
      {playlist && playlist.length > 0 && (
        <div className="playlist-tracks">
          <h3>Pistes</h3>
          <ul>
            {playlist.map((track, index) => (
              <li key={index} className="track-item">
                <span className="track-number">{index + 1}.</span>
                <div className="track-info">
                  <p className="track-title">{track.title}</p>
                  <p className="track-artist">{track.artist}</p>
                  {track.duration && (
                    <p className="track-duration">{track.duration}</p>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default PlaylistGenerator;
