const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// POST endpoint for playlist generation
app.post('/api/playlist/generate', async (req, res) => {
  try {
    const { genre, mood, artiste } = req.body;

    // Validate input
    if (!genre && !mood && !artiste) {
      return res.status(400).json({
        error: 'Au moins un paramètre est requis (genre, mood, ou artiste)'
      });
    }

    // Mock playlist data
    // TODO: Integrate with Gemini API and Supabase for real data
    const mockPlaylist = [
      {
        id: 1,
        title: `Chanson ${genre || 'populaire'} 1`,
        artist: artiste || 'Artiste inconnu',
        album: 'Album exemple',
        duration: '3:45',
        genre: genre || 'Pop',
        mood: mood || 'Joyeux',
        url: 'https://example.com/song1'
      },
      {
        id: 2,
        title: `Chanson ${genre || 'populaire'} 2`,
        artist: artiste || 'Artiste inconnu',
        album: 'Album exemple 2',
        duration: '4:12',
        genre: genre || 'Pop',
        mood: mood || 'Joyeux',
        url: 'https://example.com/song2'
      },
      {
        id: 3,
        title: `Chanson ${genre || 'populaire'} 3`,
        artist: artiste || 'Artiste inconnu',
        album: 'Album exemple 3',
        duration: '3:28',
        genre: genre || 'Pop',
        mood: mood || 'Joyeux',
        url: 'https://example.com/song3'
      },
      {
        id: 4,
        title: `Chanson ${genre || 'populaire'} 4`,
        artist: artiste || 'Artiste inconnu',
        album: 'Album exemple 4',
        duration: '4:05',
        genre: genre || 'Pop',
        mood: mood || 'Joyeux',
        url: 'https://example.com/song4'
      },
      {
        id: 5,
        title: `Chanson ${genre || 'populaire'} 5`,
        artist: artiste || 'Artiste inconnu',
        album: 'Album exemple 5',
        duration: '3:52',
        genre: genre || 'Pop',
        mood: mood || 'Joyeux',
        url: 'https://example.com/song5'
      }
    ];

    // Return the mock playlist with metadata
    res.json({
      success: true,
      playlist: mockPlaylist,
      metadata: {
        genre: genre || 'Tous',
        mood: mood || 'Tous',
        artist: artiste || 'Tous',
        totalSongs: mockPlaylist.length,
        generatedAt: new Date().toISOString()
      }
    });

  } catch (error) {
    console.error('Erreur lors de la génération de la playlist:', error);
    res.status(500).json({
      error: 'Erreur serveur lors de la génération de la playlist',
      message: error.message
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Start server
app.listen(PORT, () => {
  console.log(`Serveur en écoute sur le port ${PORT}`);
});

module.exports = app;
