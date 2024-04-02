---
name: Relatar Problema
about: Envie um relatório de problemas
title: "[Bug]: "
labels: ["bug", "triage"]
projects: ["octo-org/1", "octo-org/44"]
assignees:
    - cesarcalafrioli
body:
    - type: markdown
    attributes:
        value: |
            Obrigado pela sua contribuição!
    - type: input
    id: contact
    attributes:
        label: Detalhes do contato
        description: Informe seu email de contato. Assim, retornaremos se precisarmos de mais informações.
        placeholder: email@example.com
    validations:
        required: false
    - type: textarea
        id: what-happened
        attributes:
            label: O que aconteceu?
            description: Informe o bug ocorrido
            value: "Um bug aconteceu!"
        validations:
            required: true
    - type: dropdown
        id: version
        attributes:
            label: Version
            description: Qual versão do software você está usando?
            options:
                - 1.0 ( Padrão )
            default: 0
        validations:
            required: true
    - type: dropdown
        id: browsers
        attributes:
            label: Em quais navegadores você utilizou quando surgiu o bug?
            multiple: true
            options:
                - Firefox
                - Chrome
                - Safari
                - Microsoft Edge
    - type: textarea
        id: logs
        attributes:
            label: Log impresso
            description: Copie e cole qualquer mensagem de log relevante. Isto Será automaticamente formatado em código.
            render: shell
  - type: checkboxes
    id: terms
    attributes:
      label: Código de conduta
      description: Ao enviar essa issue, você concorda com o nosso [Código de Conduta](https://example.com)
      options:
        - label: Eu concordo com o código de conduta do projeto
          required: true

        

---

**Descreva o problema:**
Uma descrição clara e concisa do que é o problema.

**Passos para Reproduzir:**
Passos para reproduzir o comportamento:

**Comportamento Esperado:**
Uma descrição clara e concisa do que você esperava que acontecesse.

**Capturas de Tela:**
Se aplicável, adicione capturas de tela para ajudar a explicar seu problema.

**Contexto Adicional:**
Escreva qualquer contexto adicional sobre o problema aqui.
