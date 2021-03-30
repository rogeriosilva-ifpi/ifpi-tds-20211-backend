import { api } from './js/api.js';

async function carregarAnimais() {
    const lista = document.getElementById('lista_animais')
    lista.innerHTML = ''

    const response = await api.get('animais')

    const animais = response.data

    animais.forEach(animal => {
        const item = document.createElement('li')
        item.textContent = animal.nome
        lista.appendChild(item)
    });
}

function limparFormulario() {
    const form = document.getElementById('form_animal')
    form.reset()
}

async function setupForm() {
    const form = document.getElementById('form_animal')
    const inputNome = document.getElementById('nome')

    form.onsubmit = async (event) => {
        event.preventDefault()
        const nome = inputNome.value

        try {
            await api.post('/animais', {
                nome,
                idade: 7,
                sexo: 'macho',
                cor: 'Preto'
            })
            carregarAnimais()
            limparFormulario()
        } catch (e) {
            alert(`Error ao cadastrar: ${e}`)
        }

    }
}

function main() {
    carregarAnimais()
    setupForm()
}

main()