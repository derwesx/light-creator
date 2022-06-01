let onColor = '#ffff00';
let offColor = '#ffffff';

class ButtonContainer {
    methodId;
    isOn;
    isCheckBox;
    htmlButton;
    params;

    invertState() {
        if (this.isCheckBox) {
            if (this.isOn) {
                this.htmlButton.style.background = offColor
            } else {
                this.htmlButton.style.background = onColor
            }

            this.isOn = !this.isOn;
        }
    }

    executeClickQuery() {
        const data = {
            methodId: this.methodId,
            turnOn: !this.isOn,
            params: this.params,
            csrfmiddlewaretoken: $('#general_form [name="csrfmiddlewaretoken"]').val()
        };

        console.log(data)

        $.ajax({
            type: 'POST',
            url: $('#general_form').attr('action'),
            data: data,
            success: function (data) {
                console.log(data)
            }
        });
    }

    processClick() {
        this.executeClickQuery()
        this.invertState()
    }

    handleEvent(event) {
        switch (event.type) {
            case 'click':
                this.processClick();
                break;
        }
    }

    constructor(htmlButton, options, methodId, params = []) {
        this.isOn = false
        this.htmlButton = htmlButton
        this.params = params.toString()
        this.methodId = methodId
        this.isCheckBox = options.isCheckBox

        this.htmlButton.addEventListener('click', this)
        this.htmlButton.value = options.name
    }
}

function registerButton(options, params = [], methodId = options.id) {
    buttons.set(options.id, new ButtonContainer(document.getElementById(options.id), options, methodId, params))
}

function registerGroupButtons() {
    for (let i = 0; i < groupButtonOptions.length; i++) {
        registerButton(groupButtonOptions[i], [i + 1], 'group')
    }
}

function registerNoParamButtons(buttonOptions) {
    for (let i = 0; i < buttonOptions.length; i++) {
        registerButton(buttonOptions[i])
    }
}

function registerAllButtons() {
    registerGroupButtons()
    registerNoParamButtons(sceneButtonOptions)
    registerNoParamButtons(colorButtonOptions)
    registerNoParamButtons(systemButtonOptions)
    registerNoParamButtons(modeButtonOptions)
    registerNoParamButtons(effectButtonOptions)
    registerNoParamButtons(positionButtonOptions)
}

const buttons = new Map()
registerAllButtons()
