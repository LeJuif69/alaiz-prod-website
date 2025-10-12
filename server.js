const express = require('express');
const app = express();

// Configuration et routes de votre application
// Ajoutez ici vos middlewares et routes Express

if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
  });
}

module.exports = app;
