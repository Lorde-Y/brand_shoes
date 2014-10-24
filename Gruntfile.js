module.exports = function(grunt) {
// Load all grunt tasks automatically
require('load-grunt-tasks')(grunt);
// Time how long grunt task take. Can help when optimizing build times
require('time-grunt')(grunt);
//Configure grunt
grunt.initConfig({
        //css 压缩
        cssmin: {
                minify: {
                    expand: true, // 启用下面的选项
                    cwd: 'css/', // 指定待压缩的文件路径
                    src: ['*.css', '!*.min.css'], // 匹配相对于cwd目录下的所有css文件(排除.min.css文件)
                    dest: 'css/', // 生成的压缩文件存放的路径
                    ext: '.min.css' // 生成的文件都使用.min.css替换原有扩展名，生成文件存放于dest指定的目录中
                }
        },
        //less文件
        less:{
              build:{
                    options:{
                    style:'compressed'
                    },
                    files:{
                    'css/style.css':'css/style.less'
                     },
                 }
            },
        // The actual grunt server settings
        connect: {
              options: {
                    port: 9000,
                    hostname: 'localhost',
                    livereload: 35729
              },
              all: {
                      options: {
                      open: true,
                      // base: [
                      // 'examples'
                      // ]
                  }
              }
        },
        watch: {
              css:{
                  files: ['css/style.css'],
                  tasks: ['cssmin']
              },
            lesses:{
                  files: ['css/style.less'],
                  tasks: ['less']
             },
        livereload: {
                options: {
                  livereload: '<%= connect.options.livereload %>'
                },
        // Watch whatever files you needed.
        files: [
                //监测 要 更新的文件
                'index.html',
                'css/{,*/}*.css',
                'css/(,*/}*.less',
                // 'examples/styles/{,*/}*.css',
                // 'examples/scripts/(,*/}*.js',
                // 'examples/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}'
              ]
           },
         }
        });
        // Creates the 'serve' task
        grunt.registerTask('serve', [
             'connect:all',
              'watch'
        ]);
};