from miniagent import app, configure

app.run(host="0.0.0.0", port=configure['PORT'], use_reloader=False, debug=True)