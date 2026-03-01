---
name: axios
description: Make HTTP requests using axios via Node.js one-liners or scripts.
---

# axios

Use axios for HTTP requests (GET, POST, PUT, DELETE, etc.) via Node.js.

## Quick one-liners

### GET request

```bash
node -e "const axios = require('axios'); axios.get('https://api.example.com/data').then(r => console.log(JSON.stringify(r.data, null, 2))).catch(e => console.error(e.message))"
```

### POST request with JSON body

```bash
node -e "
const axios = require('axios');
axios.post('https://api.example.com/items', {
  name: 'Test',
  value: 42
}, {
  headers: { 'Content-Type': 'application/json' }
}).then(r => console.log(JSON.stringify(r.data, null, 2)))
  .catch(e => console.error(e.response?.data || e.message));
"
```

### With custom headers (e.g. Authorization)

```bash
node -e "
const axios = require('axios');
axios.get('https://api.example.com/protected', {
  headers: { 'Authorization': 'Bearer \$TOKEN' }
}).then(r => console.log(JSON.stringify(r.data, null, 2)))
  .catch(e => console.error(e.response?.status, e.message));
"
```

## Using environment variables

Access env vars via `process.env`:

```bash
node -e "
const axios = require('axios');
const url = process.env.COORDINATOR_URL + '/internal/google/gmail/send';
const token = process.env.INTERNAL_SERVICE_TOKEN;
axios.post(url, {
  user_id: 'demo-user',
  to: 'test@example.com',
  subject: 'Hello',
  body: 'Test message'
}, {
  headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }
}).then(r => console.log(r.data))
  .catch(e => console.error(e.response?.data || e.message));
"
```

## Writing to a script file

For complex requests, write a script:

```bash
cat > /tmp/request.js << 'EOF'
const axios = require('axios');

async function main() {
  try {
    const { data } = await axios.get('https://httpbin.org/get');
    console.log(JSON.stringify(data, null, 2));
  } catch (err) {
    console.error('Request failed:', err.message);
    process.exit(1);
  }
}

main();
EOF

node /tmp/request.js
```

## Notes

- axios is installed globally in the container
- Use `JSON.stringify(r.data, null, 2)` for pretty-printed output
- Access response status via `r.status`, headers via `r.headers`
- Error responses are in `e.response.data` and `e.response.status`
- For binary data, set `responseType: 'arraybuffer'`
