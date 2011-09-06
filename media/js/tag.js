/**
 * Created by TasteOfHome.
 * User: peter
 * Date: 8/14/11
 * Time: 1:34 AM
 * To change this template use File | Settings | File Templates.
 */
(function($){
    var app = $.sammy('#marker', function(){
        this.post('/tag/:key/#markmap', function(context){
            alert(this.params['key']);
        });
    });
    
    $(function(){
       app.run();
    });
})(jQuery);