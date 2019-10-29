//Variables needed in the fragment shader, varying variables that are sent
//from the vertex shader and uniform variables set in my main program through Shaders.py
varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;

varying vec2 v_uv;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;
uniform vec4 u_light_ambient; //Skipta ut fyrir global amb???

uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform vec4 u_mat_ambient;


//Taka út eða breyta ef við ætlum að nota textures.
uniform sampler2D u_tex01;
uniform sampler2D u_tex02;

uniform float u_using_texture;
uniform float u_using_specular_texture;

uniform float u_mat_shininess;

void main(void)
{
		vec4 mat_diffuse = u_mat_diffuse;
    	vec4 mat_specular = u_mat_specular;

	//Muna gera annað if/breytu til að geta notað texture sem specular
	if(u_using_texture == 1.0){
    	mat_diffuse *= texture2D(u_tex01, v_uv);
	}
	if(u_using_specular_texture == 1.0) {
		mat_specular *= texture2D(u_tex02, v_uv);
	}

	float s_len = length(v_s);
	float h_len = length(v_h);
	float n_len = length(v_normal);
	float lambert = max(dot(v_normal, v_s) / (n_len * s_len), 0.0);
	float phong = max(dot(v_normal, v_h) / (n_len * h_len), 0.0);

    gl_FragColor = u_light_ambient //* u_mat_ambient
				 + u_light_diffuse * mat_diffuse * lambert 
				 + u_light_specular * mat_specular * pow(phong, u_mat_shininess);
}