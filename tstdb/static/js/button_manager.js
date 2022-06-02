let onColor = '#ffff00';
let offColor = '#ffffff';

class ButtonContainer {
    methodId;
    isOn;
    isCheckBox;
    htmlButton;
    params;
    inputEventType;

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
            params: this.params.toString(),
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
            case this.inputEventType:
                this.processClick();
                break;
        }
    }

    setInputEventType() {
        this.inputEventType = 'click'
    }

    constructor(htmlButton, options, methodId, params = []) {
        this.setInputEventType()
        this.isOn = false
        this.htmlButton = htmlButton
        this.params = params
        this.methodId = methodId
        this.isCheckBox = options.isCheckBox

        this.htmlButton.addEventListener(this.inputEventType, this)
        this.htmlButton.value = options.name
    }
}

class SliderContainer extends ButtonContainer {
    constructor(htmlButton, options, methodId, params = []) {
        super(htmlButton, options, methodId, params);
    }

    setInputEventType() {
        this.inputEventType = 'input'
    }

    processClick() {
        this.params = [this.htmlButton.value]
        super.processClick();
    }
}

function registerButton(options, params = [], methodId = options.id) {
    buttons.set(options.id, new ButtonContainer(document.getElementById(options.id), options, methodId, params))
}

function registerSlider(options, methodId = options.id) {
    buttons.set(options.id, new SliderContainer(document.getElementById(options.id), options, methodId))
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

function registerSliders() {
    for (let i = 0; i < slidersOptions.length; i++) {
        registerSlider(slidersOptions[i])
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
    registerSliders()
}

const buttons = new Map()
registerAllButtons()
