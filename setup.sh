mkdir -p ~/.streamlit/

echp "\
[server]\n\
port = $PORT\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml