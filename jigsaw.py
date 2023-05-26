from miniagent import app, configure

#jason
port=configure.get('PORT') or 8304

app.run(host="0.0.0.0", port=port, use_reloader=False, debug=True)