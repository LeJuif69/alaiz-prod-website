import React, { useState } from 'react';

const PlaylistGenerator = () => {
  const [playlist, setPlaylist] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Nouveaux états pour les champs input contrôlés
  const [genre, setGenre] = useState('');
  const [mood, setMood] = useState('');
  const [artiste, setArtiste] = useState('');

  const generatePlaylist = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Envoi des paramètres utilisateur à l'API
      const response = await fetch('/api/playlist/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          genre: genre,
          mood: mood,
          artist: artiste,
        }),
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

  // Bouton dynamique : désactivé si tous les champs sont vides ou en cours de chargement
  const isButtonDisabled = loading || (!genre && !mood && !artiste);

  return (
    <div className="playlist-generator">
      <h2>Générateur de Playlist</h2>
      
      {/* Trois champs input contrôlés */}
      <div className="input-controls">
        <div className="input-group">
          <label htmlFor="genre">Genre:</label>
          <input
            id="genre"
            type="text"
            value={genre}
            onChange={(e) => setGenre(e.target.value)}
            placeholder="Ex: Rock, Jazz, Pop..."
            className="input-field"
          />
        </div>

        <div className="input-group">
          <label htmlFor="mood">Mood:</label>
          <input
            id="mood"
            type="text"
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            placeholder="Ex: Énergique, Calme, Joyeux..."
            className="input-field"
          />
        </div>

        <div className="input-group">
          <label htmlFor="artiste">Artiste:</label>
          <input
            id="artiste"
            type="text"
            value={artiste}
            onChange={(e) => setArtiste(e.target.value)}
            placeholder="Ex: The Beatles, Daft Punk..."
            className="input-field"
          />
        </div>
      </div>
      
      {/* Bouton dynamique */}
      <button
        onClick={generatePlaylist}
        disabled={isButtonDisabled}
        className="btn-generate"
      >
        {loading ? 'Génération en cours...' : 'Générer une playlist'}
      </button>
      
      {error && (
        <div className="error-message">
          Erreur: {error}
        </div>
      )}
      
      {/* Affichage des métadonnées */}
      {metadata && (
        <div className="playlist-metadata">
          <h3>Métadonnées</h3>
          <div className="metadata-info">
            <p>Titre: {metadata.title}</p>
            <p>Description: {metadata.description}</p>
            <p>Nombre de pistes: {metadata.trackCount}</p>
          </div>
        </div>
      )}
      
      {/* Affichage de la playlist */}
      {playlist && playlist.length > 0 && (
        <div className="playlist-tracks">
          <h3>Pistes</h3>
          <ul>
            {playlist.map((track, index) => (
              <li className="track-item" key={index}>
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
