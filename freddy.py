from miniagent import app, configure

#freddy
port=configure.get('PORT') or 8302

app.run(host="0.0.0.0", port=port, use_reloader=False, debug=True)