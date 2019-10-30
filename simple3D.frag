//Variables needed in the fragment shader, varying variables that are sent
//from the vertex shader and uniform variables set in my main program through Shaders.py
varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;

varying vec4 v_s_sun;
varying vec4 v_h_sun;

varying vec4 v_s_moon;
varying vec4 v_h_moon;

varying vec2 v_uv;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;
uniform vec4 u_global_ambient;

uniform vec4 u_sun_diffuse;
uniform vec4 u_sun_specular;
uniform vec4 u_sun_ambient;

uniform vec4 u_moon_diffuse;
uniform vec4 u_moon_specular;
uniform vec4 u_moon_ambient;

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

	if(u_using_texture == 1.0){
    	mat_diffuse *= texture2D(u_tex01, v_uv);
	}
	if(u_using_specular_texture == 1.0) {
		mat_specular *= texture2D(u_tex02, v_uv);
	}

	float s_len = length(v_s);
	float h_len = length(v_h);

	float s_sun_len = length(v_s_sun);
	float h_sun_len = length(v_h_sun);

	float s_moon_len = length(v_s_moon);
	float h_moon_len = length(v_h_moon);

	float n_len = length(v_normal);

	float lambert = max(dot(v_normal, v_s) / (n_len * s_len), 0.0);
	float phong = max(dot(v_normal, v_h) / (n_len * h_len), 0.0);

	float sun_lambert = max(dot(v_normal, v_s_sun) / (n_len * s_sun_len), 0.0);
	float sun_phong = max(dot(v_normal, v_h_sun) / (n_len * h_sun_len), 0.0);

	float moon_lambert = max(dot(v_normal, v_s_moon) / (n_len * s_moon_len), 0.0);
	float moon_phong = max(dot(v_normal, v_h_moon) / (n_len * h_moon_len), 0.0);


    gl_FragColor = u_global_ambient //* u_mat_ambient
				 + u_light_diffuse * mat_diffuse * lambert
				 + u_light_specular * mat_specular * pow(phong, u_mat_shininess)
				 //+ (u_sun_ambient
				 + u_sun_diffuse * mat_diffuse * sun_lambert
				 + u_sun_specular * mat_specular * pow(sun_phong, u_mat_shininess)
				 + u_moon_diffuse * mat_diffuse * moon_lambert
				 + u_moon_specular * mat_specular * pow(moon_phong, u_mat_shininess);
}