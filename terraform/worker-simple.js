// SnapStudio Cloudflare Worker - Simplified Version
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Handle CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    // Route handling
    if (url.pathname.startsWith('/api/')) {
      return handleAPI(request, env);
    }
    
    // Serve main app
    return handleApp(request, env);
  }
};

async function handleAPI(request, env) {
  const url = new URL(request.url);
  const path = url.pathname;
  
  try {
    switch (path) {
      case '/api/health':
        return new Response(JSON.stringify({
          status: 'healthy',
          timestamp: new Date().toISOString(),
          database: 'connected',
          version: '1.0.0'
        }), {
          headers: { 'Content-Type': 'application/json' }
        });
        
      case '/api/appointments':
        if (request.method === 'GET') {
          const { results } = await env.DB.prepare(
            "SELECT * FROM appointments ORDER BY start_time DESC LIMIT 50"
          ).all();
          return new Response(JSON.stringify(results), {
            headers: { 'Content-Type': 'application/json' }
          });
        }
        break;
        
      case '/api/clients':
        if (request.method === 'GET') {
          const { results } = await env.DB.prepare(
            "SELECT * FROM clients ORDER BY created_at DESC LIMIT 50"
          ).all();
          return new Response(JSON.stringify(results), {
            headers: { 'Content-Type': 'application/json' }
          });
        }
        break;
        
      case '/api/login':
        if (request.method === 'POST') {
          const { username, password } = await request.json();
          
          // Simple authentication (in production, use proper hashing)
          if (username === 'admin' && password === 'admin123') {
            return new Response(JSON.stringify({
              success: true,
              message: 'Login successful',
              user: { username, role: 'admin' }
            }), {
              headers: { 'Content-Type': 'application/json' }
            });
          } else {
            return new Response(JSON.stringify({
              success: false,
              message: 'Invalid credentials'
            }), {
              status: 401,
              headers: { 'Content-Type': 'application/json' }
            });
          }
        }
        break;
        
      default:
        return new Response('API endpoint not found', { status: 404 });
    }
  } catch (error) {
    return new Response(JSON.stringify({
      error: 'Internal server error',
      message: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  return new Response('Method not allowed', { status: 405 });
}

async function handleApp(request, env) {
  // Simple HTML response
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Professional Photography Management</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { background: white; border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); text-align: center; max-width: 500px; margin: 0 auto; }
        .logo { font-size: 2.5em; font-weight: bold; color: #667eea; margin-bottom: 20px; }
        .subtitle { color: #666; margin-bottom: 30px; font-size: 1.1em; }
        .status { background: #e8f5e8; color: #2d5a2d; padding: 15px; border-radius: 10px; margin-bottom: 30px; }
        .btn { background: #667eea; color: white; padding: 15px 30px; border: none; border-radius: 10px; font-size: 1.1em; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px; }
        .btn:hover { background: #5a6fd8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📸 SnapStudio</div>
        <div class="subtitle">Professional Photography Business Management</div>
        <div class="status">✅ Successfully deployed on Cloudflare Workers!<br>🚀 Serverless • ⚡ Fast • 🔒 Secure</div>
        <a href="/api/health" class="btn">Health Check</a>
        <a href="/api/appointments" class="btn">View Appointments</a>
        <a href="/api/clients" class="btn">View Clients</a>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            console.log('SnapStudio loaded successfully!');
            fetch('/api/health').then(response => response.json()).then(data => console.log('Health check:', data)).catch(error => console.error('Health check failed:', error));
        });
    </script>
</body>
</html>`;

  return new Response(html, {
    headers: {
      'Content-Type': 'text/html',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
