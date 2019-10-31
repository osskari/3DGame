varying vec2 v_uv;

uniform sampler2D u_tex01;

void main(void)
{

	vec4 color = texture2D(u_tex01, v_uv);

    gl_FragColor = color;
	gl_FragColor.a = 1.0;
}