<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A Laiz Prod - Excellence musicale camerounaise</title>
    <meta name="description" content="A Laiz Prod - Label musical camerounais alliant tradition africaine et modernité. Production musicale, événements, formation artistique.">
    <meta name="keywords" content="musique camerounaise, production musicale, label, tradition, modernité, événements, formation artistique">
    <meta name="author" content="A Laiz Prod">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://alaizprod.com/">
    <meta property="og:title" content="A Laiz Prod - Excellence musicale camerounaise">
    <meta property="og:description" content="Label musical camerounais alliant tradition africaine et modernité. Production musicale, événements, formation artistique.">
    <meta property="og:image" content="{{ url_for('static', filename='images/og-image.jpg') }}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://alaizprod.com/">
    <meta property="twitter:title" content="A Laiz Prod - Excellence musicale camerounaise">
    <meta property="twitter:description" content="Label musical camerounais alliant tradition africaine et modernité. Production musicale, événements, formation artistique.">
    <meta property="twitter:image" content="{{ url_for('static', filename='images/og-image.jpg') }}">
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Montserrat:wght@500;600&family=Open+Sans&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Analytics -->
    {% if google_analytics_id %}
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ google_analytics_id }}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '{{ google_analytics_id }}');
    </script>
    {% endif %}
    
    <!-- Facebook Pixel -->
    {% if facebook_pixel_id %}
    <script>
      !function(f,b,e,v,n,t,s)
      {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};
      if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
      n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t,s)}(window, document,'script',
      'https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', '{{ facebook_pixel_id }}');
      fbq('track', 'PageView');
    </script>
    <noscript>
      <img height="1" width="1" style="display:none" 
           src="https://www.facebook.com/tr?id={{ facebook_pixel_id }}&ev=PageView&noscript=1"/>
    </noscript>
    {% endif %}
</head>
<body>
    <!-- Header & Navigation -->
    <header class="header">
        <div class="container">
            <div class="logo">
                <a href="#accueil">A Laiz Prod</a>
            </div>
            <nav class="nav">
                <ul class="nav-list">
                    <li><a href="#accueil">Accueil</a></li>
                    <li><a href="#label">Le Label</a></li>
                    <li><a href="#pedagogie">Pédagogie</a></li>
                    <li><a href="#blog">Blog</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
                <div class="hamburger">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </nav>
        </div>
    </header>

    <main>
        <!-- Hero Section -->
        <section id="accueil" class="hero">
            <div class="hero-overlay"></div>
            <div class="container">
                <div class="hero-content">
                    <h1>A Laiz Prod</h1>
                    <p class="tagline">L'excellence musicale camerounaise – Un pont entre tradition et modernité</p>
                    <div class="cta-buttons">
                        <a href="#label" class="btn btn-primary">Découvrir nos services</a>
                        <a href="#contact" class="btn btn-secondary">Nous contacter</a>
                    </div>
                </div>
            </div>
        </section>

        <!-- Le reste du contenu reste inchangé -->
        <!-- ... -->

    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>A Laiz Prod</h3>
                    <p>L'excellence musicale camerounaise – Un pont entre tradition et modernité.</p>
                    <div class="social-links">
                        <a href="{{ facebook_url }}" target="_blank" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                        <a href="{{ instagram_url }}" target="_blank" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="{{ youtube_url }}" target="_blank" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
                        <a href="{{ linkedin_url }}" target="_blank" aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a>
                        <a href="{{ whatsapp_url }}" target="_blank" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <h4>Navigation</h4>
                    <ul>
                        <li><a href="#accueil">Accueil</a></li>
                        <li><a href="#label">Le Label</a></li>
                        <li><a href="#pedagogie">Pédagogie</a></li>
                        <li><a href="#blog">Blog</a></li>
                        <li><a href="#contact">Contact</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Coordonnées</h4>
                    <div class="contact-info">
                        <p><i class="fas fa-phone"></i> {{ director_phone }}</p>
                        <p><i class="fas fa-envelope"></i> {{ contact_email }}</p>
                        <p><i class="fas fa-calendar-alt"></i> {{ booking_email }}</p>
                    </div>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2023 A Laiz Prod. Tous droits réservés.</p>
            </div>
        </div>
    </footer>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
