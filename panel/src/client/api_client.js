export default class ApiClient {
    constructor(api_url) {
      this.url = api_url;
    }
  
    getData() {
        return fetch(`${this.url}/analyzes`)
        .then(response => response.json());
    }

    uploadFile(file, name){
        const data = new FormData()
        data.append('file', file)
        data.append('name', name)

        return fetch(`${this.url}/analyze_file`, {
            method: 'POST',
            body: data
        }).then(resp => resp.json())
    }
}
