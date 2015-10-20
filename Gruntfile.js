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
                    'src/static/bower_components/bourbon/app/assets/stylesheets',
                    'src/static/bower_components/neat/app/assets/stylesheets'
                ]
            },
            compile: {
                files: {
                    'src/static/css/screen.css': 'src/sass/screen.scss'
                },
            },
            dist: {
                files: {
                    'src/static/css/screen.css': 'src/sass/screen.scss'
                },
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
