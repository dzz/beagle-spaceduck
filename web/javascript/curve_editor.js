var CurveEditor = {

    methods: {
        drawGrid: function(w, h) {
            var ctx = this.context;
            ctx.fillStyle="#212121";
            ctx.fillRect( 0,0, this.canvas.width, this.canvas.height );

            ctx.strokeStyle = "#DDDDDD";
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo( this.center_x, 0 );
            ctx.lineTo( this.center_x, this.height );
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo( 0, this.center_y );
            ctx.lineTo( this.width, this.center_y );
            ctx.stroke();

            ctx.strokeStyle = "#010101";
            ctx.setLineDash( [3,1] );
            ctx.beginPath();
            ctx.strokeRect( 0 + this.margin_ratio*this.width, 
                            0 + this.margin_ratio*this.height,
                            this.width - (this.margin_ratio*this.width*2),
                            this.height - (this.margin_ratio*this.height*2) ); 
            
        },

        initialize: function() {
            this.canvas = $(this.el).find(".curveEditorCanvas")[0];

            this.width = this.canvas.width;
            this.height = this.canvas.height;
            this.center_x = this.width/2;
            this.center_y = this.height/2;
            this.margin_ratio = 0.1;
            this.context = this.canvas.getContext("2d");

            this.drawGrid( 16, 9 );
        }
    }
};

function curve_editor_init(id) {
    owner = $(id)[0];
    owner.CurveEditor = {};
    owner.CurveEditor.el = owner;

    _.each( _.keys( CurveEditor.methods),(key)=> {
        owner["CurveEditor"][key] = CurveEditor.methods[key];
    });
    owner.CurveEditor.initialize();
}
