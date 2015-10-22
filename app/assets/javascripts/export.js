//var export_h2o_fonts;  //TODO: deprecate
var all_tts;
var annotations;
var original_data = {};
var layer_data;
var collage_id;
var tocId = 'toc';
var h2o_annotator;
var all_collage_data = {};
var page_width_inches = 8.5;
var ignore_theme_change = false;
var cookies = [
    'hidden_text_display',
    'print_annotations',
    'print_font_face',
    'print_font_size',
    'print_highlights',
    'print_margin_size',
    'print_paragraph_numbers',
    'print_titles',
    'toc_levels',
]
var h2o_themes = {
    'default' : {
        '#toc_levels': '5',
        '#printtitle': 'yes',
        '#printparagraphnumbers': 'no',
        '#fontface': 'garamond',
        '#fontsize': 'medium',
        '#margin-top': '0.75in',
        '#margin-right': '0.75in',
        '#margin-bottom': '0.75in',
        '#margin-left': '0.75in',
    },
    'classic' : {
        '#toc_levels': '5',
        '#printtitle': 'yes',
        '#printparagraphnumbers': 'no',
        '#fontface': 'garamond',
        '#fontsize': 'large',
        '#margin-top': '1.0in',
        '#margin-right': '1.5in',
        '#margin-bottom': '1.0in',
        '#margin-left': '0.75in',
    },
    'modern' : {
        '#toc_levels': '5',
        '#printtitle': 'yes',
        '#printparagraphnumbers': 'no',
        '#fontface': 'futura',
        '#fontsize': 'medium',
        '#margin-top': '0.75in',
        '#margin-right': '0.75in',
        '#margin-bottom': '0.75in',
        '#margin-left': '0.75in',
    },
};

var collages = {
  listenToRecordAnnotatedItemState: function() {},
  set_highlights: function(data) {},
  set_highlights_for_highlight_only: function(data) {},
  rehighlight: function() {},
  updateWordCount: function() {},
  clean_layer: function(layer_name) {
    //Note: Implemented in multiple areas in our javascript/ruby
    if(layer_name === undefined) {
      return '';
    }
    return layer_name.replace(/ /g, 'whitespace').replace(/\./g, 'specialsymbol').replace(/'/g, 'apostrophe').replace(/\(/g, 'leftparen').replace(/\)/g, 'rightparen').replace(/,/g, 'c0mma').replace(/\&/g, 'amp3r');
  },
  getHexes: function() {
    return $('<div>');
  },
  loadState: function(collage_id, data) {
    export_functions.highlightAnnotatedItem(collage_id, data.highlights, data.highlight_only_highlights);

    var cannotations = all_collage_data["collage" + collage_id].annotations;
    $.each(cannotations, function(i, ann) {
      var annotation = $.parseJSON(ann);
      if(annotation.annotation != '' && !annotation.hidden && !annotation.error && !annotation.discussion && !annotation.feedback) {
        $('<span>').addClass('annotation-content annotation-content-' + annotation.id).html(annotation.annotation).insertAfter($('.annotation-' + annotation.id + ':last'));
      } else if(annotation.link !== undefined && annotation.link !== null) {
        var link_html = '<a href="' + annotation.link + '">' + annotation.link + '</a>'; 
        $('<span>').addClass('annotation-content annotation-content-' + annotation.id).html(link_html).insertAfter($('.annotation-' + annotation.id + ':last'));
      }
    });

    if($('#printannotations').val() == 'yes') {
      $('#collage' + collage_id + ' span.annotation-content').show();
    }
    if($('#printlinks').val() == 'yes') {
      $('#collage' + collage_id + ' span.annotation-content').show();
    }
    if($('#hiddentext').val() == 'show') {
      $('#collage' + collage_id + ' .layered-ellipsis-hidden').hide();
      $('#collage' + collage_id + ' .original_content,#collage' + collage_id + ' .annotation-hidden').show();
    }
    if($('#printhighlights').val() == 'all') {
      export_functions.highlightAnnotatedItem(collage_id, all_collage_data["collage" + collage_id].layer_data, all_collage_data["collage" + collage_id].highlights_only);
    }
  }
};

var export_functions = {
    set_toc: function(levels) {
        var toc_node = $('#' + tocId);
        toc_node.remove();
        if (levels) {
            export_functions.generate_toc(levels);
            $('#toc-container').show();
        } else {
            $('#toc-container').hide();
        }
    },
    generate_toc: function(toc_levels) {
        var toc_nodes = export_functions.build_toc_branch();
        var flat_results = export_functions.flatten(toc_nodes)
        var toc = $('<ol/>', { id: tocId });
        var toc_root_node = $('#toc-container');
        for(var i = 0; i<flat_results.length; i++) {
            var toc_line = export_functions.toc_entry_text(flat_results[i])
          toc.append($('<li/>', { html: toc_line }));
            toc.appendTo(toc_root_node);
        }

    },
    build_toc_branch: function(parent, depth) {
        parent = parent || $(':root');
        depth = depth || 1;
        var max_depth = $('#toc_levels').val();
        var nodes = (depth == 1) ? [] : [parent];

        parent.find('.playlists > ul').first().children().each(function () {
            var child = $(this);
            child.toc_level = depth;

            if (depth == max_depth) {
                nodes.push( child );
            }
            else {
                nodes.push( export_functions.build_toc_branch( child, depth+1 ) );
            }
        });
        return nodes;
    },
    toc_entry_text: function(node) {
        var header_node = node.children('h' + node.toc_level).first();;
        var content = header_node.children('.hcontent');
        var anchor = header_node.children('.number').children('a');

        var toc_line = '<span class="toc_level' + node.toc_level + '">' + '' +
        (Array( (node.toc_level-1) * 6 )).join('&nbsp;') +
        '<a href="#' + anchor.attr('name') + '" style="color: #000000">' +
        anchor.text() + ' ' + content.text() + '</a></span>';
      return toc_line;
    },
    flatten: function(arr) {
        return arr.reduce(function (flat, toFlatten) {
            return flat.concat(Array.isArray(toFlatten) ? export_functions.flatten(toFlatten) : toFlatten);
        }, []);
    },
  initiate_collage_data: function(id, data) {
    all_collage_data["collage" + id] = data;
  },
  init_hash_detail: function() {
    if(document.location.hash.match('fontface')) {
      //Note: The "Print" icon link from a playlist will send font info in the URL hash
      var vals = document.location.hash.replace('#', '').split('-');
      for(var i in vals) {
        var font_values = vals[i].split('=');
        var name = font_values[0];
        if ((name == 'fontface' && $.cookie('print_font_face') == null) || (name == 'fontsize' && $.cookie('print_font_size') == null)) {
            $('#' + name).val(font_values[1]).change();
        }
      }
    }
  },
    title_debug: function(msg) {
        $("h1").first().text( $("h1").first().text() + ": " + msg);
        console.log('title_debug-ing the message: ' + msg);
    },
    custom_hide: function(selector) {
        //The export process needs to remove elements, not just hide them.
        if ($.cookie('export_format')) {
            //console.log('custom_hiding: ' + selector);
            $(selector).remove();
        }
    },
    set_titles_visible: function(is_visible) {
        // Hide/Show titles in a crafty way to avoid breaking the wkhtmltopdf TOC
        var new_color = is_visible ? '#000' : '#FFF';
        $('h1').css("color", new_color)
        $('h1 > .number a').css("color", new_color)
    },

    debug_cookies: function() {
        $.each(cookies, function(i, cookie) {
            var c = $.cookie(cookie);
            console.log("Cookie: " + cookie + ": " + (c == null ? '' : c));
        });
    },
    init_missing_cookies: function() {
        return;
      /*
        //TODO: Set cookies the same way they are set in user control panel or don't set them at all
        var defaults = {
            print_margin_left: 'margin-left',
            print_margin_top: 'margin-top',
            print_margin_right: 'margin-right',
            print_margin_bottom: 'margin-bottom',
        };
        Object.keys(defaults).forEach(function(name) {
            $.cookie(name, $.cookie(name) || $('#' + defaults[name]).val() );
        });

        // $('#margin-left').val($.cookie('print_margin_left') || $('#margin-left').val());
        // $('#margin-top').val($.cookie('print_margin_top') || $('#margin-left').val());
        // $('#margin-right').val($.cookie('print_margin_right') || $('#margin-left').val());
        // $('#margin-bottom').val($.cookie('print_margin_bottom') || $('#margin-left').val());
        */
    } ,
    init_user_settings: function() {
      //TODO: Do we need this? Does this do anything that can't be done with a "selected" in the HTML?
      $('#printhighlights').val('original');  //  .change();

      if($.cookie('print_titles') == 'false') {
        $('#printtitle').val('no').change();
        export_functions.set_titles_visible(false);
      }
      if($.cookie('print_paragraph_numbers') == 'false') {
          $('#printparagraphnumbers').val('no').change();
        export_functions.custom_hide('.paragraph-numbering');
        //$('.collage-content').css('padding-left', '0px');
      } else {
          //This fixes the bug that left this selectbox showing no/hide when the
          //cookie was actually true and the paragraph numbers were being displayed
          //by default
          $('#printparagraphnumbers').val('yes').change();
      }

      if($.cookie('print_annotations') == 'true') {
        $('#printannotations').val('yes').change();
      }
      if($.cookie('print_links') == 'true') {
        $('#printlinks').val('yes').change();
      }
      if($.cookie('hidden_text_display') == 'true') {
        $('#hiddentext').val('show').change();
      }
      if($.cookie('print_highlights') == 'none') {
        $('#printhighlights').val($.cookie('print_highlights')).change();
        $('.collage-content').each(function(i, el) {
          export_functions.highlightAnnotatedItem($(el).data('id'), {}, {});
        });
      }
      if($.cookie('print_highlights') == 'all') {
        $('#printhighlights').val($.cookie('print_highlights')).change();
      }
      if ($.cookie('print_font_face') !== null ) {
          $('#fontface').val($.cookie('print_font_face')).change();
      }
      if ($.cookie('print_font_size') !== null) {
          $('#fontsize').val($.cookie('print_font_size')).change();
      }
      if($.cookie('toc_levels') && $.cookie('export_format') != 'pdf') {
          $('#toc_levels').val($.cookie('toc_levels')).change();
      }

      //These newer options may not have cookies defined yet
      //TODO: finish init_missing_cookies()
      $('#margin-left').val($.cookie('print_margin_left') || $('#margin-left').val());
      $('#margin-top').val($.cookie('print_margin_top') || $('#margin-left').val());
      $('#margin-right').val($.cookie('print_margin_right') || $('#margin-left').val());
      $('#margin-bottom').val($.cookie('print_margin_bottom') || $('#margin-left').val());
      $('#margin-left').change();
  },
  init_theme_picker_listener: function() {
    $('.theme-select-trigger').change(function() {
      if (ignore_theme_change) {
        return;
      }
      $('#theme-select').val('custom');
    });
  },
  init_listeners: function() {
    $('#export-form-submit').click(function(e) {
      e.preventDefault();
      if (!$('#export_format').val()) {
        alert('Please select an export format');
        return false;
      }
      $('#export-form').submit();
    });
    $('#toc_levels').change(function() {
      export_functions.setTocLevels($(this).val());
    });
    $('#fontface').change(function() {
      export_functions.setFontPrint();
    });
    $('#fontsize').change(function() {
      export_functions.setFontPrint();
    });
    $('.margin-select').change(function() {
        export_functions.setMargins();
    });
    $('#printannotations').change(function() {
      if($(this).val() == 'yes') {
        $('.annotation-content').show();
      } else {
        $('.annotation-content').hide();
      }
    });
    $('#printlinks').change(function() {
      if($(this).val() == 'yes') {
        $('.annotation-content').show();
      } else {
        $('.annotation-content').hide();
      }
    });
      $('#printtitle').change(function() {
        var choice = $(this).val();
        export_functions.set_titles_visible(choice == 'yes');
    });
    $('#printparagraphnumbers').change(function() {
      var choice = $(this).val();
      if (choice == 'yes') {
        $('.paragraph-numbering').show();
        $('.collage-content').css('padding-left', '50px');
      }
      else {
        $('.paragraph-numbering').hide();
        $('.collage-content').css('padding-left', '0px');
      }
    });
    $('#hiddentext').change(function() {
      var choice = $(this).val();
      if(choice == 'show') {
        $('.layered-ellipsis-hidden').hide();
        $('.original_content,.annotation-hidden').show();
      }
      else if(choice == 'hide') {
        $('.layered-ellipsis-hidden').show();
        $('.annotation-hidden').hide();
        $('.annotation-hidden').parents('.original_content').filter(':not(.original_content *):not(:has(.annotator-hl:visible,.layered-ellipsis:visible))').hide();
        $.each($('.layered-ellipsis-hidden'), function(a, b) {
          var annotation_id = $(b).data('layered');
          $.each($('.annotation-' + annotation_id).parents('.original_content').filter(':not(.original_content *)'), function(i, j) {
            var has_text_node = false;
            $.each($(j).contents(), function(k, l) {
              if(l.nodeType == 3 && $(l).text() != ' ') {
                has_text_node = true;
              }
            });
            if(has_text_node) {
              $(j).show();
            }
          });
        });
      }
    });
    $('#printhighlights').change(function() {
        var choice = $(this).val();
        $('#highlight_styles').text('');
        $('.collage-content').each(function(i, el) {
            var id = $(el).data('id');
            var data = all_collage_data["collage" + id];
            var args = null;
            if(choice == 'original') {
                args = [id, data.highlights, data.highlights_only];
            } else if(choice == 'all') {
                args = [id, data.layer_data, data.highlights_only];
            } else {  //"none"
                args = [id, {}, {}];
            }
            export_functions.highlightAnnotatedItem(args[0], args[1], args[2]);
        });
    });
    $('#theme-select').change(function() {
      ignore_theme_change = true;
      export_functions.setTheme($(this).val());
      //Prevent changed form inputs' listeners from immediately changing this back to Custom.
      setTimeout(function() {ignore_theme_change = false}, 200);
    });

    //TODO: Maybe we only need this if there is no font face or font size cookie data.
    export_functions.setFontPrint();
  },  //end init_listeners
    setTheme: function(themeId) {
        if (h2o_themes[themeId]) {
            $.each(h2o_themes[themeId], function(sel, value) {
                $(sel).val(value).change();
            });
        }
    },
    setTocLevels: function(toc_levels) {
        export_functions.set_toc(toc_levels);
        //Just control the cookie from this select box until we add a user preferences control for it
        //That will also fix the path, which is incorrect for this cookie at the moment
        $.cookie('toc_levels', toc_levels);
    },
    setMargins: function() {
        //TODO SOMEDAY: Set .wrapper margin-top while also accounting for built in margin value it needs for print-options
        var div = $('.wrapper')
        div.css('margin-left', $('#margin-left').val());
        var newWidth = parseFloat(page_width_inches) - (parseFloat($('#margin-left').val()) + parseFloat($('#margin-right').val()));
        div.css('width', newWidth + 'in');
    },
  setFontPrint: function() {
    var font_face = $('#fontface').val();
    var font_size = $('#fontsize').val();
    var mapped_font_face = h2o_fonts.font_map_fallbacks[font_face];
    var base_font_size = h2o_fonts.base_font_sizes[font_face][font_size];

    $('#fontface_mapped').val(mapped_font_face);
    $('#fontsize_mapped').val(base_font_size + 'px');
    //console.log('faceMapped: ' + $('#fontface_mapped').val());
    //console.log('sizeMapped: ' + $('#fontsize_mapped').val());

    var base = 'body#' + $('body').attr('id') + ' .singleitem';
    var rules = [
      base + ' * { font-family: ' + mapped_font_face + '; font-size: ' + base_font_size + 'px; }',
      base + ' *.scale1-5 { font-size: ' + base_font_size * 1.5 + 'px; }',
      base + ' *.scale1-4 { font-size: ' + base_font_size * 1.4 + 'px; }',
      base + ' *.scale1-3 { font-size: ' + base_font_size * 1.3 + 'px; }',
      base + ' *.scale1-2 { font-size: ' + base_font_size * 1.2 + 'px; }',
      base + ' *.scale1-1 { font-size: ' + base_font_size * 1.1 + 'px; }',
      base + ' *.scale0-9 { font-size: ' + base_font_size * 0.9 + 'px; }',
      base + ' *.scale0-8,' + base + ' *.scale0-8 * { font-size: ' + base_font_size * 0.8 + 'px; }',
    ].join("\n");

    $('#additional_styles').text('');
    $.rule(rules).appendTo('#additional_styles');
  },
  loadAnnotator: function(id) {
    annotations = all_collage_data["collage" + id].annotations || {};
    layer_data = all_collage_data["collage" + id].layer_data || {};
    highlights_only = all_collage_data["collage" + id].highlights_only || {};

    var elem = $('#collage' + id + ' div.article');
    var factory = new Annotator.Factory();
    var Store = Annotator.Plugin.fetch('Store');
    var h2o = Annotator.Plugin.fetch('H2O');
    var report_options = { "report": false, "feedback": false, "discuss": false, "respond": false };
    h2o_annotator = factory.addPlugin(h2o, layer_data, highlights_only, report_options).getInstance();
    h2o_annotator.attach(elem, 'print_export_annotation');
    h2o_annotator.plugins.H2O.loadAnnotations(id, annotations, true);
  },
  filteredLayerData: function(layer_data) {
    var filtered_layer_data = {}; 
    $.each(layer_data, function(i, j) {
      filtered_layer_data[collages.clean_layer(i)] = j;
    });
    return filtered_layer_data;
  },
  highlightAnnotatedItem: function(collage_id, highlights, highlights_only) {
    var collageCssId = '#collage' + collage_id;
    highlights = highlights || {};
    highlights_only = highlights_only || [];
    layer_data = export_functions.filteredLayerData(all_collage_data["collage" + collage_id].layer_data);

    // Removing highlights from tagged + color
    var keys = new Array();
    $.each(highlights, function(i, j) {
      keys.push(collages.clean_layer(i));
    });
    $.each(layer_data, function(i, j) {
      if($.inArray(i, keys) == -1) {
        $(collageCssId + ' .layer-' + i).removeClass('highlight-' + i);
      }
    });

    //Removing highlights from color only
    $.each(all_collage_data["collage" + collage_id].highlights_only || [], function(i, j) {
      if($.inArray(j, highlights_only) == -1) {
        $(collageCssId + ' .layer-hex-' + j).removeClass('highlight-hex-' + j);
      }
    });

    $.each(highlights, function(i, j) {
      var layer_name = collages.clean_layer(i);
      $(collageCssId + ' .annotator-wrapper .layer-' + layer_name).addClass('highlight-' + layer_name);
    });
    $.each(highlights_only, function(i, j) {
      $(collageCssId + ' .annotator-wrapper .layer-hex-' + j).addClass('highlight-hex-' + j);
    });

    var total_selectors = new Array();
    $.each($(collageCssId + ' .annotator-wrapper .annotator-hl'), function(i, child) {
      var this_selector = '';
      var parent_class = '';
      var classes = $(child).attr('class').split(' ');
      for(var j = 0; j<classes.length; j++) {
        if(classes[j].match(/^highlight/)) {
          parent_class += '.' + classes[j];
        }
      }
      if(parent_class != '') {
        this_selector = parent_class;
      }

      $.each($(child).parentsUntil('.annotator-wrapper'), function(j, node) {
        if($(node).is('span.annotator-hl')) {
          var selector_class = '';
          var classes = $(node).attr('class').split(' ');
          for(var j = 0; j<classes.length; j++) {
            if(classes[j].match(/^highlight/)) {
              selector_class += '.' + classes[j];
           }
          }
          if(selector_class != '') {
            this_selector = selector_class + ' ' + this_selector;
          }
        }
      });
      if(this_selector != '') {
        total_selectors.push(this_selector.replace(/ $/, ''));
      }
    });
    var updated = {};
    for(var i = 0; i<total_selectors.length; i++) {
      updated[total_selectors[i]] = 0;
    }

    for(var i = 0; i<total_selectors.length; i++) {
      var selector = total_selectors[i];
      if(updated[selector] == 0) {
        var unique_layers = {};
        var layer_count = 0;
        var x = selector.split(' ');
        for(var a = 0; a < x.length; a++) {
          var y = x[a].split('.');
          for(var b = 0; b < y.length; b++) {
            var key = y[b].replace(/^highlight-/, '');
            if(key != '') {
              unique_layers[key] = 1;
            }
          }
        }
        var current_hex = '#FFFFFF';
        var key_length = 0;
        $.each(unique_layers, function(key, value) {
          key_length++;
        });
        var opacity = 0.6 / key_length;
        $.each(unique_layers, function(key, value) {
          var hex_arg = key.match(/^hex-/) ? key.replace(/^hex-/, '') : layer_data[key];
          current_hex = $.xcolor.opacity(current_hex, hex_arg, opacity).getHex();
        });
        $.rule(collageCssId + ' ' + selector + ' { border-bottom: 2px solid ' + current_hex + '; }').appendTo('#highlight_styles');
        updated[selector] = 1;
      }
    }
    var keys_arr = new Array();
    $.each(updated, function(key, value) {
      keys_arr.push(key);
    });
  }
};

$(document).ready(function(){
  console.log('BOOP: document.ready starting');
  //export_functions.debug_cookies();
  //export_functions.init_missing_cookies();
  export_functions.init_listeners();
  export_functions.init_hash_detail();
  export_functions.init_user_settings();

  $('article sub, article sup, div.article sub, div.article sup').addClass('scale0-8');

  // Should h1 actually be scale1-5 here? scale1-5 does seem conspicuously absent
  //   from this list, but it shows up in setFontPrint()
  $('article h1, div.article h1, .new-h1').addClass('scale1-4');
  $('article h2, div.article h2, .new-h2').addClass('scale1-3');
  $('article h3, div.article h3, .new-h3').addClass('scale1-2');
  $('article h4, div.article h4, .new-h4').addClass('scale1-1');

  $('div.article *:not(.paragraph-numbering)').addClass('original_content');
  $('.collage-content').each(function(i, el) {
    export_functions.loadAnnotator($(el).data('id')); 
  });

    if ($.cookie('export_format')) {
        // Remove things that would otherwise trip up any of our exporter backends
        $('#print-options').remove();
        $('#toc-container').show();  //TODO: Do we still need this?

        // Reset margins because export back-end will manage them
        //NEW: technically, we only need to do this for PDF exports, because PDF
        //exports set margins outside of javascript/HTML completely.

        var div = $('.wrapper');
        //TODO: maybe set margins here based on cookie value, instead of doing it in phantomjs
        /*
        div.css('margin', '');
        div.css('margin-top', '');
        div.css('margin-right', '');
        div.css('margin-bottom', '');
        div.css('margin-left', '');
        div.css('width', '');
        */
        div.removeAttr('style');  //TODO: This really replaces all the above, so delete them.
        div.css('margin-top', '0px');  //Remove margin previously occupied by #print-options

        //$('div.article *:not(.paragraph-numbering)'). <-- "not" filter example with faster selector
        //TODO: Reminder: This will remove any hidden dom nodes we want to .show() in phantomjs
        $("body *").filter(":hidden").not("script").remove();

        //PhantomJS requires this in page scope
        //export_h2o_fonts = h2o_fonts;
    }
  else {
      export_functions.init_theme_picker_listener();
  }

    console.log('BOOP: document.ready done');
});


