%if user is not None and fail is None:
      <div class="panel panel-default">
        <div class="panel-heading">Add Note</div>
        <div class="panel-body">
          <form role="form" action="/new" method="POST">
            <div class="form-group">
              <input type="title" class="form-control" id="title" placeholder="Title" name="title">
            </div>
            <div class="form-group">
              <input type="content" class="form-control" id="content" placeholder="Content" name="content">
            </div>
            <input class="btn btn-success pull-right" type="submit" value="Save Note" name="save">
          </form>
        </div>
      </div>
%elif fail is not None:
      <div class="panel panel-default">
        <div class="panel-heading">Login failed, check your credentials and try again</div>
      </div>
%else:
      <div class="panel panel-default">
        <div class="panel-heading">Sign in to add notes</div>
      </div>
%end
    </div>
  </div>
</div>
