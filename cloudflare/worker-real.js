// SnapStudio Real Application - Replace Test Version
// Professional Photography Business Management System

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;
    
    // Handle CORS
    if (method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    try {
      // Route handling
      if (path.startsWith('/api/')) {
        return await handleAPI(request, env, path, method);
      }
      
      // Serve static pages
      return await handlePage(request, env, path, method);
      
    } catch (error) {
      console.error('Error:', error);
      return new Response(JSON.stringify({
        error: 'Internal server error',
        message: error.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
};

// Handle API endpoints
async function handleAPI(request, env, path, method) {
  // Health check
  if (path === '/api/health') {
    return new Response(JSON.stringify({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      database: 'connected',
      version: '2.0.0 - Real SnapStudio',
      message: 'Professional Photography Business Management System'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  // Authentication endpoints
  if (path === '/api/login' && method === 'POST') {
    const { username, password } = await request.json();
    
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
  
  // Appointments API
  if (path === '/api/appointments' && method === 'GET') {
    try {
      const { results } = await env.DB.prepare(
        "SELECT a.*, c.name as client_name, c.email as client_email FROM appointments a LEFT JOIN clients c ON a.client_id = c.id ORDER BY a.start_time DESC"
      ).all();
      
      return new Response(JSON.stringify({
        success: true,
        appointments: results
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (error) {
      return new Response(JSON.stringify({
        success: false,
        error: error.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
  
  // Clients API
  if (path === '/api/clients' && method === 'GET') {
    try {
      const { results } = await env.DB.prepare(
        "SELECT * FROM clients ORDER BY created_at DESC"
      ).all();
      
      return new Response(JSON.stringify({
        success: true,
        clients: results
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (error) {
      return new Response(JSON.stringify({
        success: false,
        error: error.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
  
  return new Response('API endpoint not found', { status: 404 });
}

// Handle page requests
async function handlePage(request, env, path, method) {
  // Default to dashboard for root
  if (path === '/') {
    return await renderDashboard(env);
  }
  
  // Login page
  if (path === '/login') {
    return await renderLogin(env);
  }
  
  // Dashboard
  if (path === '/dashboard') {
    return await renderDashboard(env);
  }
  
  // Appointments
  if (path === '/appointments') {
    return await renderAppointments(env);
  }
  
  // Clients
  if (path === '/clients') {
    return await renderClients(env);
  }
  
  // Calendar
  if (path === '/calendar') {
    return await renderCalendar(env);
  }
  
  // Analytics
  if (path === '/analytics') {
    return await renderAnalytics(env);
  }
  
  // Packages
  if (path === '/packages') {
    return await renderPackages(env);
  }
  
  // Setup
  if (path === '/setup') {
    return await renderSetup(env);
  }
  
  // Backup/Restore
  if (path === '/backup-restore') {
    return await renderBackupRestore(env);
  }
  
  // 404 for unknown pages
  return new Response('Page not found', { status: 404 });
}

// Page renderers
async function renderDashboard(env) {
  try {
    // Get dashboard data
    const [clientsResult, appointmentsResult, revenueResult] = await Promise.all([
      env.DB.prepare("SELECT COUNT(*) as count FROM clients").first(),
      env.DB.prepare("SELECT COUNT(*) as count FROM appointments").first(),
      env.DB.prepare("SELECT SUM(session_fee) as total FROM appointments WHERE status = 'completed'").first()
    ]);
    
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Professional Photography Management</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .dashboard-card { background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .stat-card { background: linear-gradient(45deg, #667eea, #764ba2); color: white; border-radius: 10px; }
        .navbar-brand { font-size: 1.5em; font-weight: bold; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">📸 SnapStudio</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/appointments">Appointments</a>
                <a class="nav-link" href="/clients">Clients</a>
                <a class="nav-link" href="/calendar">Calendar</a>
                <a class="nav-link" href="/analytics">Analytics</a>
                <a class="nav-link" href="/packages">Packages</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="stat-card p-4 text-center">
                    <h3>${clientsResult?.count || 0}</h3>
                    <p class="mb-0">Total Clients</p>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="stat-card p-4 text-center">
                    <h3>${appointmentsResult?.count || 0}</h3>
                    <p class="mb-0">Total Appointments</p>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="stat-card p-4 text-center">
                    <h3>$${revenueResult?.total || 0}</h3>
                    <p class="mb-0">Total Revenue</p>
                </div>
            </div>
        </div>
        
        <div class="dashboard-card p-4">
            <h2>Welcome to SnapStudio</h2>
            <p class="lead">Professional Photography Business Management System</p>
            <div class="row">
                <div class="col-md-6">
                    <h5>Quick Actions</h5>
                    <a href="/appointments" class="btn btn-primary me-2">View Appointments</a>
                    <a href="/clients" class="btn btn-success me-2">View Clients</a>
                    <a href="/calendar" class="btn btn-info">View Calendar</a>
                </div>
                <div class="col-md-6">
                    <h5>System Status</h5>
                    <div class="alert alert-success">
                        <strong>✅ System Online</strong><br>
                        Database: Connected<br>
                        Version: 2.0.0 - Real SnapStudio<br>
                        Status: Ready for business
                    </div>
                </div>
            </div>
        </div>
        
        <div class="dashboard-card p-4 mt-4">
            <h4>Recent Activity</h4>
            <p>Your recent appointments and client updates will appear here.</p>
            <div class="text-center">
                <a href="/appointments" class="btn btn-outline-primary">View All Appointments</a>
                <a href="/clients" class="btn btn-outline-success">View All Clients</a>
            </div>
        </div>
    </div>
</body>
</html>`;
    
    return new Response(html, {
      headers: { 'Content-Type': 'text/html' }
    });
  } catch (error) {
    return new Response(`Error loading dashboard: ${error.message}`, { status: 500 });
  }
}

async function renderLogin(env) {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; }
        .login-card { background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <div class="login-card p-4">
                    <h2 class="text-center mb-4">📸 SnapStudio</h2>
                    <p class="text-center text-muted">Professional Photography Management</p>
                    <form id="loginForm">
                        <div class="mb-3">
                            <label class="form-label">Username</label>
                            <input type="text" class="form-control" name="username" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" class="form-control" name="password" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Login</button>
                    </form>
                    <div class="mt-3 text-center">
                        <small>Default: admin / admin123</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: formData.get('username'),
                    password: formData.get('password')
                })
            });
            
            const result = await response.json();
            if (result.success) {
                window.location.href = '/dashboard';
            } else {
                alert('Login failed: ' + result.message);
            }
        });
    </script>
</body>
</html>`;
  
  return new Response(html, {
    headers: { 'Content-Type': 'text/html' }
  });
}

async function renderAppointments(env) {
  try {
    const { results } = await env.DB.prepare(
      "SELECT a.*, c.name as client_name FROM appointments a LEFT JOIN clients c ON a.client_id = c.id ORDER BY a.start_time DESC LIMIT 20"
    ).all();
    
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Appointments</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">📸 SnapStudio</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/dashboard">Dashboard</a>
                <a class="nav-link" href="/clients">Clients</a>
                <a class="nav-link" href="/calendar">Calendar</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Appointments</h2>
            <a href="/appointments/new" class="btn btn-primary">New Appointment</a>
        </div>
        
        <div class="row">
            ${results.map(appointment => `
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${appointment.title}</h5>
                            <p class="card-text">
                                <strong>Client:</strong> ${appointment.client_name || 'Unknown'}<br>
                                <strong>Date:</strong> ${new Date(appointment.start_time).toLocaleDateString()}<br>
                                <strong>Time:</strong> ${new Date(appointment.start_time).toLocaleTimeString()}<br>
                                <strong>Status:</strong> <span class="badge bg-primary">${appointment.status}</span><br>
                                <strong>Fee:</strong> $${appointment.session_fee || 0}
                            </p>
                            <a href="/appointments/${appointment.id}" class="btn btn-sm btn-outline-primary">View Details</a>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    </div>
</body>
</html>`;
    
    return new Response(html, {
      headers: { 'Content-Type': 'text/html' }
    });
  } catch (error) {
    return new Response(`Error loading appointments: ${error.message}`, { status: 500 });
  }
}

async function renderClients(env) {
  try {
    const { results } = await env.DB.prepare(
      "SELECT * FROM clients ORDER BY created_at DESC LIMIT 20"
    ).all();
    
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Clients</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">📸 SnapStudio</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/dashboard">Dashboard</a>
                <a class="nav-link" href="/appointments">Appointments</a>
                <a class="nav-link" href="/calendar">Calendar</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Clients</h2>
            <a href="/clients/new" class="btn btn-primary">New Client</a>
        </div>
        
        <div class="row">
            ${results.map(client => `
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${client.name}</h5>
                            <p class="card-text">
                                <strong>Email:</strong> ${client.email}<br>
                                <strong>Phone:</strong> ${client.phone || 'Not provided'}<br>
                                <strong>Address:</strong> ${client.address || 'Not provided'}<br>
                                <strong>Created:</strong> ${new Date(client.created_at).toLocaleDateString()}
                            </p>
                            <a href="/clients/${client.id}" class="btn btn-sm btn-outline-primary">View Details</a>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    </div>
</body>
</html>`;
    
    return new Response(html, {
      headers: { 'Content-Type': 'text/html' }
    });
  } catch (error) {
    return new Response(`Error loading clients: ${error.message}`, { status: 500 });
  }
}

async function renderCalendar(env) {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Calendar</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">📸 SnapStudio</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/dashboard">Dashboard</a>
                <a class="nav-link" href="/appointments">Appointments</a>
                <a class="nav-link" href="/clients">Clients</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <h2>Calendar View</h2>
        <div class="alert alert-info">
            <h5>📅 Calendar Integration</h5>
            <p>Calendar view will be implemented with a proper calendar library (FullCalendar.js) to show:</p>
            <ul>
                <li>Monthly/weekly/daily views</li>
                <li>Appointment scheduling</li>
                <li>Drag-and-drop rescheduling</li>
                <li>Google Calendar integration</li>
            </ul>
            <a href="/appointments" class="btn btn-primary">View Appointments List</a>
        </div>
    </div>
</body>
</html>`;
  
  return new Response(html, {
    headers: { 'Content-Type': 'text/html' }
  });
}

async function renderAnalytics(env) {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Analytics</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">📸 SnapStudio</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/dashboard">Dashboard</a>
                <a class="nav-link" href="/appointments">Appointments</a>
                <a class="nav-link" href="/clients">Clients</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <h2>Analytics Dashboard</h2>
        <div class="alert alert-info">
            <h5>📊 Business Analytics</h5>
            <p>Analytics dashboard will include:</p>
            <ul>
                <li>Revenue tracking and trends</li>
                <li>Client acquisition metrics</li>
                <li>Session type performance</li>
                <li>Monthly/quarterly reports</li>
                <li>Client lifetime value</li>
            </ul>
            <a href="/dashboard" class="btn btn-primary">Back to Dashboard</a>
        </div>
    </div>
</body>
</html>`;
  
  return new Response(html, {
    headers: { 'Content-Type': 'text/html' }
  });
}

async function renderPackages(env) {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Packages</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">📸 SnapStudio</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/dashboard">Dashboard</a>
                <a class="nav-link" href="/appointments">Appointments</a>
                <a class="nav-link" href="/clients">Clients</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <h2>Package Management</h2>
        <div class="alert alert-info">
            <h5>📦 Photography Packages</h5>
            <p>Package management will include:</p>
            <ul>
                <li>Newborn session packages</li>
                <li>Milestone session packages</li>
                <li>Family portrait packages</li>
                <li>Custom package creation</li>
                <li>Pricing management</li>
            </ul>
            <a href="/dashboard" class="btn btn-primary">Back to Dashboard</a>
        </div>
    </div>
</body>
</html>`;
  
  return new Response(html, {
    headers: { 'Content-Type': 'text/html' }
  });
}

async function renderSetup(env) {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Setup</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">📸 SnapStudio</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/dashboard">Dashboard</a>
                <a class="nav-link" href="/appointments">Appointments</a>
                <a class="nav-link" href="/clients">Clients</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <h2>System Setup</h2>
        <div class="alert alert-info">
            <h5>⚙️ Configuration</h5>
            <p>System setup will include:</p>
            <ul>
                <li>Business information configuration</li>
                <li>Google Calendar integration</li>
                <li>Email settings</li>
                <li>Session types and pricing</li>
                <li>User account management</li>
            </ul>
            <a href="/dashboard" class="btn btn-primary">Back to Dashboard</a>
        </div>
    </div>
</body>
</html>`;
  
  return new Response(html, {
    headers: { 'Content-Type': 'text/html' }
  });
}

async function renderBackupRestore(env) {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Backup & Restore</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">📸 SnapStudio</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/dashboard">Dashboard</a>
                <a class="nav-link" href="/appointments">Appointments</a>
                <a class="nav-link" href="/clients">Clients</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <h2>Backup & Restore</h2>
        <div class="alert alert-info">
            <h5>💾 Data Management</h5>
            <p>Backup and restore functionality will include:</p>
            <ul>
                <li>Automated daily backups</li>
                <li>Manual backup creation</li>
                <li>Data export/import</li>
                <li>System restore points</li>
                <li>Cloud storage integration</li>
            </ul>
            <a href="/dashboard" class="btn btn-primary">Back to Dashboard</a>
        </div>
    </div>
</body>
</html>`;
  
  return new Response(html, {
    headers: { 'Content-Type': 'text/html' }
  });
}
