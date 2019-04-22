module.exports = function(grunt) {

    var sass_files = [
        {
            expand: true,
            cwd: 'src/sass/',
            src: ['*.scss'],
            dest: 'src/static/css/',
            ext: '.css'
        }
    ];

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            sass: {
                files: [
                    'src/sass/**/*.{scss,sass}',
                ],
                tasks: ['sass:compile']
            },
            livereload: {
                files: ['css/*.css','img/**/*.{png,jpg,jpeg,gif,webp,svg}'],
                options: {
                    livereload: true
                }
            }
        },
        sass: {
            options: {
                sourceMap: true,
                outputStyle: 'expanded',
                includePaths: [
                    'node_modules/bourbon/app/assets/stylesheets',
                    'node_modules/bourbon-neat/app/assets/stylesheets'
                ],
            },
            compile: {
                files: sass_files
            },
            dist: {
                files: sass_files,
                options: {
                    outputStyle: 'compressed',
                }
            }
        }
    });
    grunt.registerTask('default', ['sass:compile', 'watch']);

    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
};
