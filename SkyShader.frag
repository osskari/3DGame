varying vec2 v_uv;

//uniform float u_using_alpha_texture;
//Taka út eða breyta ef við ætlum að nota textures.
uniform sampler2D u_tex01;
//uniform sampler2D u_tex02;

void main(void)
{

	vec4 color = texture2D(u_tex01, v_uv);
	// if(u_using_alpha_texture == 1.0){
	// 	mat_diffuse *= ;
	// 	opacity *= 1 - texture2D(u_tex02, v_uv).r;
	// }

    gl_FragColor = color;
	gl_FragColor.a = 1.0;
}