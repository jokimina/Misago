import ReactDOM from 'react-dom';
import mount from 'misago/utils/mount-component';

export class Modal {
  init(element) {
    this._element = element;

    this._modal = $(element).modal({show: false});

    this._modal.on('hidden.bs.modal', () => {
      ReactDOM.unmountComponentAtNode(this._element);
    });
  }

  show(component, callback) {
    mount(component, this._element.id);
    this._modal.modal('show');
    if(callback&&typeof(callback)==="function"){
        this._modal.on('hide.bs.modal', callback);
    }
  }

  hide() {
    this._modal.modal('hide');
  }
}

export default new Modal();
