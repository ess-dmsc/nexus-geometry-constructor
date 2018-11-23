import QtQuick 2.11
import QtQuick.Controls 2.4
import MyValidators 1.0

Pane {

    contentWidth: listContainer.width

    Pane {
        id: headingRow
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        contentHeight: addDetector.height
        padding: 1

        Label {
            anchors.left: parent.left
            anchors.verticalCenter: addDetector.verticalCenter
            text: "Components:"
        }
        Button {
            id: addDetector
            anchors.right: parent.right

            text: "Add detector"
            onClicked: {
                if (modalLoader.source == ""){
                    modalLoader.source = "AddDetectorWindow.qml"
                    modalLoader.item.show()
                } else {
                    modalLoader.item.requestActivate()
                }
            }
            Loader {
                id: modalLoader
                Connections {
                    target: modalLoader.item
                    onClosing: modalLoader.source = ""
                }
            }
        }
    }

    Frame {
        id: listContainer
        anchors.left: parent.left
        contentWidth: componentListView.width
        anchors.top: headingRow.bottom
        anchors.bottom: parent.bottom
        padding: 1
        ListView {
            id: componentListView
            model: components
            delegate: componentDelegate
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            clip: true
        }
    }

    Component {
        id: componentDelegate
        Frame {
            id: componentBox
            padding: 5
            contentHeight: Math.max(mainContent.height, expansionCaret.height)
            contentWidth: transformControls.width

            Component.onCompleted: componentListView.width = componentBox.width

            MouseArea {
                id: expansionClickArea
                anchors.fill: parent
                onClicked: componentBox.state = (componentBox.state == "Extended") ? "": "Extended"
            }

            Image {
                id: expansionCaret
                width: 20; height: 20;
                anchors.right: parent.right
                anchors.top: parent.top
                source: "file:resources/images/caret.svg"
                transformOrigin: Item.Center
                rotation: 0
            }

            Item {
                id: mainContent
                anchors.left: parent.left
                anchors.right: parent.right
                height: mainNameLabel.height
                visible: true
                Label {
                    id: mainNameLabel
                    anchors.left: parent.left
                    anchors.top: parent.top
                    text: "Name:" + name
                }
            }

            Item {
                id: extendedContent
                anchors.top: mainContent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                height: 0
                visible: false
                Item {
                    height: nameField.height + transformControls.height + editorButton.height
                    width: parent.width
                    id: extendedText

                    LabeledTextField {
                        id: nameField
                        labelText: "Name:"
                        editorText: name
                        onEditingFinished: name = editorText
                        validator: NameValidator {
                            model: components
                            myindex: index
                            onValidationFailed: {
                                nameField.ToolTip.show("Component names must be unique", 3000)
                            }
                        }
                    }

                    TransformControls {
                        id: transformControls
                        anchors.top: nameField.bottom
                    }

                    PaddedButton {
                        id: editorButton
                        anchors.top: transformControls.bottom
                        anchors.left: parent.left
                        width: parent.width / 4
                        text: "Full editor"
                        onClicked: {
                            if (editorLoader.source == ""){
                                editorLoader.source = "EditComponentWindow.qml"
                                editorLoader.item.componentIndex = index
                                editorLoader.item.show()
                            } else {
                                editorLoader.item.requestActivate()
                            }
                        }
                    }
                    Loader {
                        id: editorLoader
                        Connections {
                            target: editorLoader.item
                            onClosing: editorLoader.source = ""
                        }
                    }
                    PaddedButton {
                        id: deleteButton
                        anchors.top: editorButton.top
                        anchors.right: parent.right
                        width: parent.width / 4
                        text: "Delete"
                        onClicked: components.remove_component(index)
                        buttonEnabled: removable
                        // The sample (at index 0) should never be removed. Don't even show it as an option.
                        visible: index != 0
                        ToolTip.visible: hovered & !removable
                        ToolTip.delay: 400
                        ToolTip.text: "Cannot remove a component that's in use as a transform parent"
                    }
                }
            }

            states: State {
                name: "Extended"

                PropertyChanges { target: mainContent; height: 0 }
                PropertyChanges { target: mainContent; visible: false }

                PropertyChanges { target: extendedContent; height: extendedText.height }
                PropertyChanges { target: extendedContent; visible: true }

                PropertyChanges { target: componentBox; contentHeight: extendedContent.height}

                PropertyChanges { target: expansionCaret; rotation: 180 }
            }
        }
    }
}
