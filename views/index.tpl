% rebase layout

% include navbar user_is_logged_in=is_logged_in

<div class="container">
  <div class="row">
    <div class="col-md-8">
% include noteslist rows=rows, user_is_logged_in=is_logged_in
    </div>
    <div class="col-md-4">
% include panel_to_add_note user_is_logged_in=is_logged_in, login_has_failed=has_failed
    </div>
  </div>
</div>
