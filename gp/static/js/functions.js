<script>
            window.onload = function() {
                const canvas = document.getElementById('oldpp_canvas');
                const ctx = canvas.getContext('2d');
                var oldpp_len = '{{oldpp_len}}';
                
                draw();
                var rectangle = new Path2D();
                var wnh = 128;
                for (let i = 0; i < 8; i++) {
                    for (let i1 = 0; i1 < 6; i1++) {
                        rectangle.rect(i*wnh, i1*wnh, 128, 128);
                        ctx.strokeStyle = 'orange';
                        ctx.stroke(rectangle);
                    }
                }
                
                function draw() {
                    // var ctx = document.getElementById('canvas').getContext('2d');
                    var img = new Image();
                    img.onload = function() {
                        ctx.drawImage(img, 0, 0);
                    };
                    img.src = 'images/oldpp_image.jpg';
                }
                }
</script>