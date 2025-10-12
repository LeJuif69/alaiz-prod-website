const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
  // Logique/fallback local (ex : retourner mock data)
  module.exports = function fetchPlaylist() {
    return Promise.resolve([
      { title: "Titre fictif 1", artist: "Demo Artist 1" },
      { title: "Titre fictif 2", artist: "Demo Artist 2" },
      { title: "Titre fictif 3", artist: "Demo Artist 3" }
    ]);
  };
} else {
  // Votre code normal avec GEMINI_API_KEY
  // TODO: Implémenter la logique avec l'API Gemini
  module.exports = function fetchPlaylist() {
    // Logique d'appel API avec apiKey
    return Promise.resolve([
      { title: "Titre depuis API", artist: "API Artist" }
    ]);
  };
}
