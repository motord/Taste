/**
 * Created by TasteOfHome.
 * User: peter
 * Date: 8/14/11
 * Time: 1:34 AM
 * To change this template use File | Settings | File Templates.
 */
(function($){
    var app = $.sammy('#marker', function(){
        this.use('Template');

        this.post('#/markmap', function(context){
            $.post('markmap', function(tag){
                context.app.swap('');
                context.render($('#tag_tmpl'), {tag: tag}).appendTo($('#map'));
            });
        });
    });
    
    $(function(){
       app.run();
    });
})(jQuery);