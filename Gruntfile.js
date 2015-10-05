module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            sass: {
                files: [
                    'src/sass/**/*.{scss,sass}',
                    'src/sass/partials/**/*.{scss,sass}',
                    'src/sass/bitters/**/*.{scss,sass}'
                ],
                tasks: ['sass:dist']
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
                    'src/static/bower_components/bourbon/app/assets/stylesheets',
                    'src/static/bower_components/neat/app/assets/stylesheets'
                ]
            },
            dist: {
                files: {
                    'src/static/css/screen.css': 'src/sass/screen.scss'
                }
            }
        }
    });
    grunt.registerTask('default', ['sass:dist', 'watch']);

    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
};
