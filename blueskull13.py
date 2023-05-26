from miniagent import app, configure

#blueskull13
port=configure.get('PORT') or 8301

app.run(host="0.0.0.0", port=port, use_reloader=False, debug=True)