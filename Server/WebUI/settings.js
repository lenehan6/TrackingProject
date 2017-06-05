/**
 * Created by jameslenehan on 05.06.17.
 */

function validateFile( input, type, submitBtn ){
    var filePath = input.value;

    var ext = filePath.substring(filePath.lastIndexOf('.') + 1).toLowerCase();
    if(ext != type) {
        if ( prompt('Only files with the file extension "*.' + type + '" are allowed. Please choose a new file.') )
            #( input ).click();
        else
            return;
    }

    submitBtn.enabled = true;
}
