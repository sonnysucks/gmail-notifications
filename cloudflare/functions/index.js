// SnapStudio Cloudflare Function
// Professional Photography Business Management System
// Migrated from Flask web application

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
  const segments = path.split('/').filter(s => s);
  
  // Authentication endpoints
  if (path === '/api/login' && method === 'POST') {
    return await handleLogin(request, env);
  }
  
  if (path === '/api/logout' && method === 'POST') {
    return await handleLogout(request, env);
  }
  
  // Health check
  if (path === '/api/health') {
    return new Response(JSON.stringify({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      database: 'connected',
      version: '2.0.0'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  // Appointments API
  if (segments[1] === 'appointments') {
    return await handleAppointmentsAPI(request, env, segments, method);
  }
  
  // Clients API
  if (segments[1] === 'clients') {
    return await handleClientsAPI(request, env, segments, method);
  }
  
  // Packages API
  if (segments[1] === 'packages') {
    return await handlePackagesAPI(request, env, segments, method);
  }
  
  // Analytics API
  if (segments[1] === 'analytics') {
    return await handleAnalyticsAPI(request, env, segments, method);
  }
  
  // Backup/Restore API
  if (segments[1] === 'backup') {
    return await handleBackupAPI(request, env, segments, method);
  }
  
  // Correspondence API
  if (segments[1] === 'correspondence') {
    return await handleCorrespondenceAPI(request, env, segments, method);
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

// Authentication handlers
async function handleLogin(request, env) {
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

async function handleLogout(request, env) {
  return new Response(JSON.stringify({
    success: true,
    message: 'Logged out successfully'
  }), {
    headers: { 'Content-Type': 'application/json' }
  });
}

// Appointments API handlers
async function handleAppointmentsAPI(request, env, segments, method) {
  if (method === 'GET' && segments.length === 2) {
    // GET /api/appointments - List all appointments
    const { results } = await env.DB.prepare(
      "SELECT a.*, c.name as client_name, c.email as client_email FROM appointments a LEFT JOIN clients c ON a.client_id = c.id ORDER BY a.start_time DESC"
    ).all();
    
    return new Response(JSON.stringify({
      success: true,
      appointments: results
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'POST' && segments.length === 2) {
    // POST /api/appointments - Create new appointment
    const data = await request.json();
    
    const result = await env.DB.prepare(
      "INSERT INTO appointments (client_id, title, start_time, end_time, status, notes, session_fee) VALUES (?, ?, ?, ?, ?, ?, ?)"
    ).bind(
      data.client_id,
      data.title,
      data.start_time,
      data.end_time,
      data.status || 'scheduled',
      data.notes || '',
      data.session_fee || 0
    ).run();
    
    return new Response(JSON.stringify({
      success: true,
      appointment_id: result.meta.last_row_id
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'GET' && segments.length === 3) {
    // GET /api/appointments/{id} - Get specific appointment
    const appointmentId = segments[2];
    const { results } = await env.DB.prepare(
      "SELECT a.*, c.name as client_name, c.email as client_email FROM appointments a LEFT JOIN clients c ON a.client_id = c.id WHERE a.id = ?"
    ).bind(appointmentId).all();
    
    if (results.length === 0) {
      return new Response(JSON.stringify({
        success: false,
        error: 'Appointment not found'
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response(JSON.stringify({
      success: true,
      appointment: results[0]
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'PUT' && segments.length === 3) {
    // PUT /api/appointments/{id} - Update appointment
    const appointmentId = segments[2];
    const data = await request.json();
    
    const result = await env.DB.prepare(
      "UPDATE appointments SET title = ?, start_time = ?, end_time = ?, status = ?, notes = ?, session_fee = ? WHERE id = ?"
    ).bind(
      data.title,
      data.start_time,
      data.end_time,
      data.status,
      data.notes,
      data.session_fee,
      appointmentId
    ).run();
    
    return new Response(JSON.stringify({
      success: true,
      updated: result.meta.changes > 0
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'DELETE' && segments.length === 3) {
    // DELETE /api/appointments/{id} - Delete appointment
    const appointmentId = segments[2];
    
    const result = await env.DB.prepare(
      "DELETE FROM appointments WHERE id = ?"
    ).bind(appointmentId).run();
    
    return new Response(JSON.stringify({
      success: true,
      deleted: result.meta.changes > 0
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  return new Response('Method not allowed', { status: 405 });
}

// Clients API handlers
async function handleClientsAPI(request, env, segments, method) {
  if (method === 'GET' && segments.length === 2) {
    // GET /api/clients - List all clients
    const { results } = await env.DB.prepare(
      "SELECT * FROM clients ORDER BY created_at DESC"
    ).all();
    
    return new Response(JSON.stringify({
      success: true,
      clients: results
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'POST' && segments.length === 2) {
    // POST /api/clients - Create new client
    const data = await request.json();
    
    const result = await env.DB.prepare(
      "INSERT INTO clients (name, email, phone, address, notes) VALUES (?, ?, ?, ?, ?)"
    ).bind(
      data.name,
      data.email,
      data.phone || '',
      data.address || '',
      data.notes || ''
    ).run();
    
    return new Response(JSON.stringify({
      success: true,
      client_id: result.meta.last_row_id
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'GET' && segments.length === 3) {
    // GET /api/clients/{id} - Get specific client
    const clientId = segments[2];
    const { results } = await env.DB.prepare(
      "SELECT * FROM clients WHERE id = ?"
    ).bind(clientId).all();
    
    if (results.length === 0) {
      return new Response(JSON.stringify({
        success: false,
        error: 'Client not found'
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response(JSON.stringify({
      success: true,
      client: results[0]
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'PUT' && segments.length === 3) {
    // PUT /api/clients/{id} - Update client
    const clientId = segments[2];
    const data = await request.json();
    
    const result = await env.DB.prepare(
      "UPDATE clients SET name = ?, email = ?, phone = ?, address = ?, notes = ? WHERE id = ?"
    ).bind(
      data.name,
      data.email,
      data.phone,
      data.address,
      data.notes,
      clientId
    ).run();
    
    return new Response(JSON.stringify({
      success: true,
      updated: result.meta.changes > 0
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'DELETE' && segments.length === 3) {
    // DELETE /api/clients/{id} - Delete client
    const clientId = segments[2];
    
    const result = await env.DB.prepare(
      "DELETE FROM clients WHERE id = ?"
    ).bind(clientId).run();
    
    return new Response(JSON.stringify({
      success: true,
      deleted: result.meta.changes > 0
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  return new Response('Method not allowed', { status: 405 });
}

// Packages API handlers
async function handlePackagesAPI(request, env, segments, method) {
  if (method === 'GET' && segments.length === 2) {
    // GET /api/packages - List all packages
    const { results } = await env.DB.prepare(
      "SELECT * FROM packages ORDER BY name"
    ).all();
    
    return new Response(JSON.stringify({
      success: true,
      packages: results
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'GET' && segments[2] === 'active') {
    // GET /api/packages/active - List active packages
    const { results } = await env.DB.prepare(
      "SELECT * FROM packages WHERE active = 1 ORDER BY name"
    ).all();
    
    return new Response(JSON.stringify({
      success: true,
      packages: results
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  return new Response('Packages API endpoint not implemented', { status: 501 });
}

// Analytics API handlers
async function handleAnalyticsAPI(request, env, segments, method) {
  if (method === 'GET' && segments[2] === 'revenue') {
    // GET /api/analytics/revenue - Revenue analytics
    const { results } = await env.DB.prepare(
      "SELECT SUM(session_fee) as total_revenue, COUNT(*) as total_sessions FROM appointments WHERE status = 'completed'"
    ).all();
    
    return new Response(JSON.stringify({
      success: true,
      revenue: results[0]
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  return new Response('Analytics API endpoint not implemented', { status: 501 });
}

// Backup API handlers
async function handleBackupAPI(request, env, segments, method) {
  return new Response('Backup API endpoint not implemented', { status: 501 });
}

// Correspondence API handlers
async function handleCorrespondenceAPI(request, env, segments, method) {
  return new Response('Correspondence API endpoint not implemented', { status: 501 });
}

// Page renderers
async function renderDashboard(env) {
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
    <title>SnapStudio - Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .dashboard-card { background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .stat-card { background: linear-gradient(45deg, #667eea, #764ba2); color: white; border-radius: 10px; }
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
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="stat-card p-4 text-center">
                    <h3>${clientsResult.count}</h3>
                    <p class="mb-0">Total Clients</p>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="stat-card p-4 text-center">
                    <h3>${appointmentsResult.count}</h3>
                    <p class="mb-0">Total Appointments</p>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="stat-card p-4 text-center">
                    <h3>$${revenueResult.total || 0}</h3>
                    <p class="mb-0">Total Revenue</p>
                </div>
            </div>
        </div>
        
        <div class="dashboard-card p-4">
            <h2>Welcome to SnapStudio</h2>
            <p>Professional Photography Business Management System</p>
            <div class="row">
                <div class="col-md-6">
                    <h5>Quick Actions</h5>
                    <a href="/appointments/new" class="btn btn-primary me-2">New Appointment</a>
                    <a href="/clients/new" class="btn btn-success me-2">New Client</a>
                    <a href="/calendar" class="btn btn-info">View Calendar</a>
                </div>
                <div class="col-md-6">
                    <h5>Recent Activity</h5>
                    <p>Recent appointments and client updates will appear here.</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>`;
  
  return new Response(html, {
    headers: { 'Content-Type': 'text/html' }
  });
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
}

async function renderClients(env) {
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
            Calendar view will be implemented with a proper calendar library.
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
        <h2>Analytics</h2>
        <div class="alert alert-info">
            Analytics dashboard will be implemented with charts and detailed metrics.
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
        <h2>Packages</h2>
        <div class="alert alert-info">
            Package management will be implemented with full CRUD operations.
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
        <h2>Setup</h2>
        <div class="alert alert-info">
            System setup and configuration will be implemented.
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
            Backup and restore functionality will be implemented.
        </div>
    </div>
</body>
</html>`;
  
  return new Response(html, {
    headers: { 'Content-Type': 'text/html' }
  });
}
