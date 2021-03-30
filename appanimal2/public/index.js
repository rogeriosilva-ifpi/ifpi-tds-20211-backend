async function carregarAnimais() {
    const response = await axios.get('http://localhost:8000/animais')

    const animais = response.data

    const lista = document.getElementById('lista-animais')

    lista.innerHTML = ''

    animais.forEach(animal => {
        const item = document.createElement('li')

        const linha = `${animal.nome} - idade: ${animal.idade} - cor: ${animal.cor}`

        item.innerText = linha

        lista.appendChild(item)
    });

}

function manipularFormulario() {
    const form_animal = document.getElementById('form-animal')
    const input_nome = document.getElementById('nome')

    form_animal.onsubmit = async (event) => {
        event.preventDefault()
        const nome_animal = input_nome.value

        await axios.post('http://localhost:8000/animais', {
            nome: nome_animal,
            idade: 4,
            sexo: 'femea',
            cor: 'branco'
        })

        carregarAnimais()
        alert('Animal cadastrado..')
    }
}

function app() {
    console.log('App iniciada')
    carregarAnimais()
    manipularFormulario()
}

app()